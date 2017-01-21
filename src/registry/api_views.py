from rest_framework import generics
from . import models
from . import serializers
import logging

logger = logging.getLogger('django')

class ApiIOVIew(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.IOModel.objects.all()
    serializer_class = serializers.IOSerializer

class ApiIOSimpleView(generics.ListCreateAPIView):
    queryset = models.IOModel.objects.all()
    serializer_class = serializers.IOSimpleSerializer

    def perform_create(self, serializer):
        logger.info("in create")
        logger.info(serializer.validated_data)

        kwargs = {}

        category = self.request.data.get('category')
        if category is not None:
            kwargs['category'] = models.CategoryModel.objects.get(name=category)

        payment_method = self.request.data.get('payment_method')
        if payment_method is not None:
            kwargs['payment_method'] = models.PaymentMethodModel.objects.get(name=payment_method)
        else:
            kwargs['payment_method'] = models.PaymentMethodModel.objects.get(name='mBank')


        amount = serializer.validated_data['amount']
        kwargs['amount'] = abs(amount)
        kwargs['type'] = models.IOModel.INCOME if amount >= 0 else models.IOModel.OUTCOME

        serializer.save(**kwargs)

class ApiCategoryView(generics.ListAPIView):
    queryset = models.CategoryModel.objects.all()
    serializer_class = serializers.CategorySerializer

class ApiPaymentMethodView(generics.ListAPIView):
    queryset = models.PaymentMethodModel.objects.all()
    serializer_class = serializers.PaymentMethodSerializer