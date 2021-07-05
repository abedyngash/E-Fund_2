from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ApplicantResource

# Register your models here.
@admin.register(Subcounty)
class SubcountyAdminView(ImportExportModelAdmin):
	search_fields = ['name']

@admin.register(Ward)
class WardAdminView(ImportExportModelAdmin):
	list_display = ['name', 'subcounty']
	search_fields = ['name']

@admin.register(Sublocation)
class SublocationAdminView(admin.ModelAdmin):
	list_display = ['name', 'ward', 'subcounty']
	search_fields = ['name']

@admin.register(SchoolType)
class SchoolTypeAdminView(admin.ModelAdmin):
	list_display = ['name', 'amount_allocated']
	search_fields = ['name']

@admin.register(Applicant)
class ApplicantAdminView(ImportExportModelAdmin):
	resource_class = ApplicantResource
	list_display = ['first_name', 'last_name', 'financial_year']
	search_fields = ['first_name', 'last_name', 'financial_year']

@admin.register(School)
class SchoolAdminView(ImportExportModelAdmin):
	search_fields = ['name']
