from django.contrib import admin
from .models import Item
from django.contrib.admin.filters import AllValuesFieldListFilter

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_filter= ['date_updated', ('condition', AllValuesFieldListFilter)]

admin.site.register(Item, ItemAdmin)