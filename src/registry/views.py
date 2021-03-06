# -*- coding: utf-8 -*-

import datetime
import logging

from collections import OrderedDict, defaultdict

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.dateparse import parse_date

from .models import IOModel, CategoryModel, BillingCycleModel
from .forms import IOForm, ListIOFilter, ImportIOForm, PaymentMethodModel
from .reports import OverviewReport
from .import_parser import MBankCsvParser, MBANK_FILTERS

logger = logging.getLogger('django')
# class Referer(object):
# 	refererFieldName = 'referer'
# 	def __init__(self, request, default=None):
# 		self.__referer = request.session.pop( # removing it
# 			self.refererFieldName,
# 			request.POST.get(
# 				self.refererFieldName,
# 				request.GET.get(
# 					self.refererFieldName,
# 					request.META.get('HTTP_REFERER')
# 				)
# 			)
# 		)
# 		if self.__referer is None:
# 			self.__referer = default
# 
# 	def get(self):
# 		return self.__referer

class IndexView(View):
	def post(self, request):
		form = IOForm(request.POST)
		if form.is_valid():
			io = form.save()
			io.save()
			return HttpResponseRedirect(reverse('registry:index'))
		else:
			return render(request, r'registry/index.html', self._make_context_with_form(form))

	def get(self, request):
		context = self._make_context_with_form(IOForm())
		context.update({'import_form': ImportIOForm()})
		return render(
			request,
			r'registry/index.html',
			context
		)

	def _make_context_with_form(self, form):
		return {
			'form' : form,
			'ios' : IOModel.objects.order_by('-updated')[:10]
		}

class ImportIOView(View):
    def post(self, request):
        form = ImportIOForm(request.POST, request.FILES)
        if form.is_valid():
            data = MBankCsvParser().parse(request.FILES['io_file'])
            data = self._filter(data)
            return render(request, r'registry/import.html', dict(data=data, categories=CategoryModel.objects.all()))
        else:
            return render(request, r'registry/import.html', dict(error="Failed to import selected file."))

    def _filter(self, data):
        result = []
        for d in data:
            for filter in MBANK_FILTERS:
                d = filter(d)
                if d is None: break
            if d is not None:
                result.append(d)
        return result


class BillingsView(View):
	def get(self, request):
		billings = BillingCycleModel.objects.all().order_by('-start_date')
		report = None
		if len(billings) != 0:
			report = OverviewReport(billings[0].start_date, billings[0].end_date)
		return render(request, r'registry/billings.html', {'billings': billings, 'report': report})


class ListIOView(View):
	def get(self, request):
		filter = ListIOFilter(request.GET, queryset=IOModel.objects.all().order_by('registered'))
		query = request.GET.copy()
		ios = self.paginate(filter.qs, int(query.pop('page', [1])[-1]), 100)

		return render(request, r'registry/list_io.html', {'ios': ios, 'filter': filter, 'query': query})

# 	def post(self, request):
# 		filter = ListIOFilter(request.POST, queryset=IOModel.objects.all().order_by('registered'))
# 		ios = self.paginate(filter.qs, request.GET.get('page'))
# 		return render(request, r'registry/list_io.html', {'ios': ios, 'filter': filter})

	def paginate(self, queryset, page, pageSize):
		paginator = Paginator(queryset, pageSize)
		try:
			result = paginator.page(page)
		except PageNotAnInteger:
			result = paginator.page(1)
		except EmptyPage:
			result = paginator.page(paginator.num_pages)
		return result


class DeleteIOView(View):
	def get(self, request, id):
		answer = request.GET.get('answer')
		if answer:
			if answer == 'yes':
				IOModel.objects.get(pk=id).delete()
			return HttpResponseRedirect(request.session.pop('referer', reverse('registry:index')))
		else:
			request.session['referer'] = request.META.get('HTTP_REFERER', reverse('registry:index'))
			return render(request, r'registry/delete_io.html', {'io' : IOModel.objects.get(pk=id)})


class EditIOView(View):
	def post(self, request, id):
		form = IOForm(request.POST, instance=IOModel.objects.get(pk=id))
		if form.is_valid():
			io = form.save()
			io.save()
			return HttpResponseRedirect(request.session.pop('referer', reverse('registry:index')))
		else:
			return render(request, r'registry/edit_io.html', {'form': form, 'io_id': id})

	def get(self, request, id):
		form = IOForm(instance=IOModel.objects.get(pk=id))
		request.session['referer'] = request.META.get('HTTP_REFERER', reverse('registry:index'))
		return render(request, r'registry/edit_io.html', {'form': form, 'io_id': id})


class ReportView(View):
	def get(self, request):
		return render(request, r'registry/report.html')

class ReportViewView(View):
	def get(self, request):
		start_date = parse_date(request.GET.get('start_date'))
		end_date = parse_date(request.GET.get('end_date', str(datetime.date.today())))
		order_by = request.GET.get('order_by', 'registered')

		# TODO both above can be None, report only error in that case

		ios = IOModel.objects.filter(
			registered__gte=start_date,
			registered__lte=end_date
		).order_by(order_by)

		total = defaultdict(lambda: 0)
		category_transfers = defaultdict(lambda: defaultdict(lambda: 0))

		for io in ios:
			transfer_type = 'income' if io.type == IOModel.INCOME else 'outcome'

			total[transfer_type] += io.amount

			category_name = io.category.name if io.category is not None else '_inne_'
			separator_position = category_name.find(CategoryModel.NAMESPACE_SEPARATOR)
			while separator_position != -1:
				category_part = category_name[:separator_position]
				category_transfers[category_part][transfer_type] += io.amount
				separator_position = category_name.find(CategoryModel.NAMESPACE_SEPARATOR, separator_position + 1)
			category_transfers[category_name][transfer_type] += io.amount

		return render(
			request, r'registry/report_view.html',
			{
				'ios': ios,
				'start_date': start_date,
				'end_date': end_date,
				'total': total,
				'category_transfers': OrderedDict(sorted(category_transfers.items(), key=lambda item: item[0].lower)),
			}
		)

class BillingView(View):
	def get(self, request, id):
		billing = BillingCycleModel.objects.get(pk=id)
		report = OverviewReport(billing.start_date, billing.end_date)
		return render(request, r'registry/billing_view.html', {'name': billing.name, 'report': report})