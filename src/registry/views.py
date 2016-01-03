from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import IOModel
from .forms import IOForm

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
			'ios' : IOModel.objects.order_by('-registered')[:10]
		}

	
class ListIOView(View):
	def get(self, request):
		return render(request, r'registry/list_io.html', {'ios': IOModel.objects.all()})


class DeleteIOView(View):
	def get(self, request, id):
		IOModel.objects.get(pk=id).delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('registry:index')))
