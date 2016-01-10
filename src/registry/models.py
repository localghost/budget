from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class PaymentMethodModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'payment method'
        verbose_name_plural = 'payment methods'
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CategoryModel(models.Model):
    NAMESPACE_SEPARATOR = r'/'
    
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
     
    def __str__(self):
        return self.name
    

@python_2_unicode_compatible
class IOModel(models.Model):
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
    registered = models.DateTimeField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BillingModel(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(unique=True)
    end_date = models.DateField(blank=True, null=True, unique=True)
    
    class Meta:
        ordering = ['start_date']
        verbose_name = 'billing'
        verbose_name_plural = 'billings'
        
    def __str__(self):
        return self.name