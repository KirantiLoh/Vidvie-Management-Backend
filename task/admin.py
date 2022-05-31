from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from rangefilter.filters import DateRangeFilter
from .models import Task
from import_export.admin import ExportActionMixin
from .resources import TaskResource

# Register your models here.
class TaskAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = (('priority', AllValuesFieldListFilter), ('status', AllValuesFieldListFilter), ('date_added', DateRangeFilter))
    resource_class = TaskResource

admin.site.register(Task, TaskAdmin)
