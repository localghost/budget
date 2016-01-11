from django.forms import ModelForm
from models import IOModel, CategoryModel, PaymentMethodModel
from django.db.models.functions import Lower
# from django import forms
import django_filters
# import datetime

class IOForm(ModelForm):
    class Meta:
        model = IOModel
        fields = ['name', 'type', 'amount', 'registered', 'category', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(IOForm, self).__init__(*args, **kwargs)   
        self.fields['category'].queryset = CategoryModel.objects.order_by(Lower('name'))
        self.fields['payment_method'].queryset = PaymentMethodModel.objects.order_by(Lower('name'))


# class ListIOFilterForm(forms.Form):
#     start_date = forms.DateField(required=False, label="Od")
#     end_date = forms.DateField(required=False, label="Do")
#     type = forms.ChoiceField(required=False, label="Typ")
#     category = forms.ModelChoiceField(required=False, queryset=CategoryModel.objects.all(), label="Kategoria")
#     
#     def __init__(self, *args, **kwargs):
#         self.label_suffix = ':'
#         
#         super(ListIOFilterForm, self).__init__(*args, **kwargs)
#         
#         self.fields['type'].choices = (('', '--------'),) + IOModel.TYPE_CHOICES
        
class ListIOFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(lookup_type='gte', label="Od", help_text='', name='registered')
    end_date = django_filters.DateFilter(lookup_type='lte', label="Do", help_text='', name='registered')
    type = django_filters.ChoiceFilter(label="Typ", help_text='')
    category = django_filters.ModelChoiceFilter(queryset=CategoryModel.objects.all(), label="Kategoria", help_text='')
    
    class Meta:
        model = IOModel
        fields = []
        
    def __init__(self, *args, **kwargs):
        super(ListIOFilter, self).__init__(*args, **kwargs)
        self.form.label_suffix = ':'
        self.form.fields['type'].choices = (('', '--------'),) + IOModel.TYPE_CHOICES
