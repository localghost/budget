from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import BillModel
from .forms import BillForm

class IndexView(View):
	def post(self, request):
		form = BillForm(request.POST)
		if form.is_valid():
			bill = form.save()
			bill.save()
			return HttpResponseRedirect(reverse('bills:index'))
		else:
			return render(request, r'bills/index.html', self._make_context_with_form(form))
		
	def get(self, request):
		return render(request, r'bills/index.html', self._make_context_with_form(BillForm()))
	
	def _make_context_with_form(self, form):
		return {
			'form' : form,
			'bills' : BillModel.objects.order_by('-spent')[:10]
		}

	
class ListBillsView(View):
	def get(self, request):
		return render(request, r'bills/list_bills.html', {'bills': BillModel.objects.all()})
