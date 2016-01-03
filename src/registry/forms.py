from django.forms import ModelForm
from models import BillModel

class BillForm(ModelForm):
    class Meta:
        model = BillModel
        fields = ['name', 'type', 'amount', 'spent', 'category', 'payment_method']