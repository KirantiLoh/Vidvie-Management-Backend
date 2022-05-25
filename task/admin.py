from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_filter = (('priority', AllValuesFieldListFilter), ('status', AllValuesFieldListFilter))

admin.site.register(Task, TaskAdmin)
