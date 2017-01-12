"""budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import api_views

app_name = 'registry'


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^billings$', views.BillingsView.as_view(), name='billings'),
    url(r'^list_io$', views.ListIOView.as_view(), name='list_io'),
    url(r'^io/delete/(?P<id>\d+)/$', views.DeleteIOView.as_view(), name='delete_io'),
    url(r'^io/edit/(?P<id>\d+)/$', views.EditIOView.as_view(), name='edit_io'),
    url(r'^report$', views.ReportView.as_view(), name='report'),
    url(r'^report/view$', views.ReportViewView.as_view(), name='report_view'),
    url(r'^billing/view/(?P<id>\d+)/$', views.BillingView.as_view(), name='billing/view'),
    url(r'^import$', views.ImportIOView.as_view(), name='import')
]

apiurls = [
    url(r'^api/io/$', api_views.ApiIOVIew.as_view(), name='api-io'),
    url(r'^api/io-simple/$', api_views.ApiIOSimpleView.as_view(), name='api-io-simple'),
    url(r'^api/category/$', api_views.ApiCategoryView.as_view(), name='api-category'),
    url(r'^api/payment-method/$', api_views.ApiPaymentMethodView.as_view(), name='api-payment-method'),
]

urlpatterns += format_suffix_patterns(apiurls)
