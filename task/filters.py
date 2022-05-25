from asyncio import Task
import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    date_added = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Task
        fields = ['priority', 'status', 'date_added']