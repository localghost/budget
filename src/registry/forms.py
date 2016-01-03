from django.forms import ModelForm
from models import IOModel

class IOForm(ModelForm):
    class Meta:
        model = IOModel
        fields = ['name', 'type', 'amount', 'registered', 'category', 'payment_method']