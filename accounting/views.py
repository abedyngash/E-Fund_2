from django.shortcuts import render
import datetime
from django.views.generic import ListView, CreateView, UpdateView
from . import models as accounting_models
from applications import models as applications_models
from django.forms import ModelForm
from django.db.models import Count, Sum
# from applications import filters as applications_filters


# Create your views here.
def get_money_per_ward():
	money_per_ward = 0
	wards = applications_models.Ward.objects.all().count()
	number_of_wards = int(wards)
	obj = accounting_models.AllocationDetail.objects.all().get(financial_year__start_date=datetime.date.today().year, financial_year__end_date=datetime.date.today().year+1)
	field = 'amount_allocated'

	if obj:
		money_per_ward = int(getattr(obj, field) / number_of_wards)
	return money_per_ward

def get_current_financial_year():
	start_year = datetime.date.today().year
	end_year = datetime.date.today().year+1

	start_year_string = str(start_year)
	end_year_string  = str(end_year)

	financial_year_string = start_year_string + "/" + end_year_string
	# print(financial_year_string)

	return financial_year_string

def allocationdetails(request):
	schooltypes = applications_models.SchoolType.objects.all()
	tags = ['success', 'danger', 'warning', 'secondary', 'primary']
	schooltypes_with_tags =zip(schooltypes, tags)
	context = {
		'title': 'Allocations',
		'current_year_allocation' : accounting_models.AllocationDetail.objects.all().get(financial_year__start_date=str(datetime.date.today().year), financial_year__end_date=str(datetime.date.today().year+1)),
		'wards' : applications_models.Ward.objects.all().count(),
		'subcounties' : applications_models.Subcounty.objects.all().count(),
		'schooltypes_with_tags': schooltypes_with_tags,
		'money_per_ward' : get_money_per_ward(),
	}
	return render(request, 'accounting/allocation_list.html', context)

# def allocationdetailsupdate(request, id):

#     object_ = accounting_models.AllocationDetail.objects.get(id=id)
#     form = ModelForm(instance=object_)

#     return render(request, 'accounting/allocation_form.html', {'form':form})

def disbursements_view(request):
	context = {
		'title': 'Disbursements',
	}
	return render(request, 'accounting/disbursements/disbursements_home.html', context)
