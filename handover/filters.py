from dataclasses import fields
import django_filters
from .models import HandOver

class HandOverFilter(django_filters.FilterSet):
    date_added = django_filters.DateFromToRangeFilter()
    class Meta:
        model = HandOver
        fields = ['date_added', 'is_approved']