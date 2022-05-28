import django_filters
from .models import Item

class ItemFilter(django_filters.FilterSet):
    date_added = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Item
        fields = ('date_added', 'condition')
