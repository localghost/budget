from rest_framework import serializers
from . import models

class IOSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IOModel
        fields = '__all__'

class IOSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IOModel
        fields = ['amount', 'registered', 'name']