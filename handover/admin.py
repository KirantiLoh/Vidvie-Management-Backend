from django.contrib import admin
from .models import HandOver

# Register your models here.
class HandOverAdmin(admin.ModelAdmin):
    list_display = ['tipe', 'item', 'count', 'requestor', 'requestor_division', 'requestee_division']
    list_select_related = ['item', 'requestor', 'requestor_division', 'requestee_division']
    search_fields =['item', 'requestor']
    list_filter = ['tipe','requestee_division', 'requestor_division']

admin.site.register(HandOver, HandOverAdmin)