from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FinancialYear)

@admin.register(AllocationDetail)
class AllocationsAdmin(admin.ModelAdmin):
	list_display =['financial_year', 'amount_allocated', 'application_start_date', 'application_end_date']

admin.site.register(Cheque)