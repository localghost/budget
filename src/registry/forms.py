from django.forms import ModelForm
from models import IOModel, CategoryModel, PaymentMethodModel
from django.db.models.functions import Lower

class IOForm(ModelForm):
    class Meta:
        model = IOModel
        fields = ['name', 'type', 'amount', 'registered', 'category', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(IOForm, self).__init__(*args, **kwargs)   
        self.fields['category'].queryset = CategoryModel.objects.order_by(Lower('name'))
        self.fields['payment_method'].queryset = PaymentMethodModel.objects.order_by(Lower('name'))