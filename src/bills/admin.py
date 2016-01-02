from django.contrib import admin

from .models import CategoryModel, PaymentMethodModel

admin.site.register(CategoryModel)
admin.site.register(PaymentMethodModel)