from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from rangefilter.filters import DateRangeFilter
from .models import Task
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resources import TaskResource

# Register your models here.
class TaskAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'requestor_division', 'requestee_division', 'date_added')
    list_select_related = ('requestor_division', 'requestee_division')
    list_filter = (('priority', AllValuesFieldListFilter), ('status', AllValuesFieldListFilter), ('date_added', DateRangeFilter))
    resource_class = TaskResource
    search_fields = ['title',]

admin.site.register(Task, TaskAdmin)
