# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 12:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bills.Category'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bills.PaymentMethod'),
        ),
    ]
