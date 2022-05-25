from django.contrib import admin
from .models import Division, Account

# Register your models here.
class DivisionAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    list_filter = ('division',)

admin.site.register(Division, DivisionAdmin)
admin.site.register(Account, AccountAdmin)
