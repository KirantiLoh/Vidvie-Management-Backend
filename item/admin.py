from django.contrib import admin

from item.resources import ItemResource
from .models import Item
from django.contrib.admin.filters import AllValuesFieldListFilter
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'condition', 'stock', 'date_added', 'date_updated')
    list_filter= ['date_updated', ('condition', AllValuesFieldListFilter)]
    resource_class = ItemResource
    search_fields = ['name',]

admin.site.register(Item, ItemAdmin)