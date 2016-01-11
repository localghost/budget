import datetime
import collections

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.utils.dateparse import parse_date

from .models import IOModel, CategoryModel, BillingCycleModel
from .forms import IOForm, ListIOFilterForm
from .reports import OverviewReport

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
		return render(request, r'registry/index.html', self._make_context_with_form(IOForm()))
	
	def _make_context_with_form(self, form):
		return {
			'form' : form,
			'ios' : IOModel.objects.order_by('-updated')[:10]
		}

	
class BillingsView(View):
	def get(self, request):
		billings = BillingCycleModel.objects.all().order_by('-start_date')
		report = None
		if len(billings) != 0:
			report = OverviewReport(billings[0].start_date, billings[0].end_date)
		return render(request, r'registry/billings.html', {'billings': billings, 'report': report})
	

class ListIOView(View):
	def get(self, request):
		form = ListIOFilterForm(initial={'end_date': datetime.datetime.now().strftime('%Y-%m-%d')})
		return render(request, r'registry/list_io.html', {'ios': IOModel.objects.all().order_by('registered'), 'form': form})
	
	def post(self, request):
		form = ListIOFilterForm(request.POST)
		if form.is_valid():
			filter_args = {}
			if form.cleaned_data['start_date']:
				filter_args['registered__gte'] = form.cleaned_data['start_date']
			if form.cleaned_data['end_date']:
				filter_args['registered__lte'] = form.cleaned_data['end_date']
			if form.cleaned_data['category']:
				filter_args['category_id'] = int(form.cleaned_data['category'])
			ios = IOModel.objects.filter(**filter_args).order_by('registered')
		else:
			ios = IOModel.objects.all().order_by('registered')
		return render(request, r'registry/list_io.html', {'ios': ios, 'form': form})


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
		
		total_outcome = total_income = 0
		category_outcome = {}
		
		for io in ios:
			if io.type == IOModel.INCOME:
				total_income += io.amount
			elif io.type == IOModel.OUTCOME:
				total_outcome += io.amount
				separator_position = io.category.name.find(CategoryModel.NAMESPACE_SEPARATOR)
				while separator_position != -1:
					amount = category_outcome.get(io.category.name[:separator_position], 0)
					category_outcome[io.category.name[:separator_position]] = amount + io.amount
					separator_position = io.category.name.find(CategoryModel.NAMESPACE_SEPARATOR, separator_position + 1)
				amount = category_outcome.get(io.category.name, 0)
				category_outcome[io.category.name] = amount + io.amount

		return render(
			request, r'registry/report_view.html',
			{
				'ios': ios,
				'start_date': start_date,
				'end_date': end_date,
				'total_outcome': total_outcome,
				'total_income': total_income,
				'total_balance': total_income - total_outcome,
				'category_outcome' : collections.OrderedDict(sorted(category_outcome.items(), key=lambda t: t[0])),
			}
		)

class BillingView(View):
	def get(self, request, id):
		billing = BillingCycleModel.objects.get(pk=id)
		report = OverviewReport(billing.start_date, billing.end_date)
		return render(request, r'registry/billing_view.html', {'name': billing.name, 'report': report})