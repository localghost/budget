from django.contrib import admin

from .models import CategoryModel, PaymentMethodModel, BillingCycleModel

admin.site.register(CategoryModel)
admin.site.register(PaymentMethodModel)
admin.site.register(BillingCycleModel)