from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class PaymentMethodModel(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class CategoryModel(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class BillModel(models.Model):
    INCOME = 'I'
    OUTCOME = 'O'
    TYPE_CHOICES = (
        (INCOME, 'Income'),
        (OUTCOME, 'Outcome')
    )
    
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    payment_method = models.ForeignKey(
        PaymentMethodModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=OUTCOME)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    spent = models.DateTimeField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name