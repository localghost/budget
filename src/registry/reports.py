import datetime

from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible

from models import IOModel, CategoryModel

class GeneralReport(object):
    def __init__(self, start_date, end_date = datetime.date.today()):
        pass

@python_2_unicode_compatible    
class OverviewReport(object):
    def __init__(self, start_date, end_date = None):
        self.__start_date = start_date
        self.__end_date = end_date
        if self.__end_date is None:
            self.__end_date = datetime.date.today()
        self.__closed = end_date is not None
            
    @property
    def start_date(self):
        return self.__start_date
    
    @property
    def end_date(self):
        return self.__end_date
    
    @property
    def closed(self):
        return self.__closed
    
    @property
    def incomes(self):
        return IOModel.objects.filter(
            type = IOModel.INCOME,
            registered__gte=self.__start_date,
            registered__lte=self.__end_date).order_by('registered')

    @property
    def categories(self):
        ios = IOModel.objects.filter(
            type = IOModel.OUTCOME,
            registered__gte=self.__start_date,
            registered__lte=self.__end_date).order_by('registered')
        
        categories = {}
        for io in ios:
            name = io.category.name.split(CategoryModel.NAMESPACE_SEPARATOR)[0]
            categories[name] = categories.get(name, 0) + io.amount

        return categories
    
    def __str__(self):
        return render_to_string(r'registry/overview_report.html', {'report': self})