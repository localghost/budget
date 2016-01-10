from django.contrib import admin

from .models import CategoryModel, PaymentMethodModel, BillingModel

admin.site.register(CategoryModel)
admin.site.register(PaymentMethodModel)
admin.site.register(BillingModel)