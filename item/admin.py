from django.contrib import admin
from item.resources import ItemResource
from .models import Item
from django.contrib.admin.filters import AllValuesFieldListFilter
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from rangefilter.filters import DateTimeRangeFilter

# Register your models here.
class ItemAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'division', 'condition', 'stock', 'borrowed', 'broken', 'date_added', 'date_updated')
    list_filter= [('date_updated', DateTimeRangeFilter), ('condition', AllValuesFieldListFilter), 'division']
    resource_class = ItemResource
    search_fields = ['name',]

admin.site.register(Item, ItemAdmin)