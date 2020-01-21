from .models import Applicant, Subcounty, Ward, Sublocation, SchoolType
import django_filters
from django_select2.forms import *
from applications.models import HistoricalApplicant

class SubcountyWidget(ModelSelect2Widget):
    model = Subcounty
    search_fields = [
        'name__icontains',
    ]

class WardWidget(ModelSelect2Widget):
    model = Ward
    search_fields = [
        'name__icontains',
    ],
    dependent_fields={'subcounty': 'subcounty'}

class SublocationWidget(ModelSelect2Widget):
    model = Sublocation
    search_fields = [
        'name__icontains',
    ],
    dependent_fields={'subcounty': 'subcounty', 'ward': 'ward'}

class SchoolFilter(django_filters.FilterSet):
	subcounty = django_filters.ModelChoiceFilter(
        queryset=Subcounty.objects.all(),
        widget= SubcountyWidget
    )
	ward = django_filters.ModelChoiceFilter(
	    queryset=Ward.objects.all(),
	    label='Ward',
	    widget=ModelSelect2Widget(
	  queryset=Ward.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	sublocation = django_filters.ModelChoiceFilter(
	    queryset=Sublocation.objects.all(),
	    label='Sublocation',
	    widget=ModelSelect2Widget(
	  queryset=Sublocation.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty', 'ward': 'ward'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	school_type = django_filters.ModelChoiceFilter(
		queryset = SchoolType.objects.all(),
		widget=Select2Widget
		)
	class Meta:
		model = Applicant
		fields = ['subcounty', 'ward', 'sublocation', 'school_type']

class ApplicantFilter(django_filters.FilterSet):
	subcounty = django_filters.ModelChoiceFilter(
        queryset=Subcounty.objects.all(),
        widget= SubcountyWidget
    )
	ward = django_filters.ModelChoiceFilter(
	    queryset=Ward.objects.all(),
	    label='Ward',
	    widget=ModelSelect2Widget(
	  queryset=Ward.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	sublocation = django_filters.ModelChoiceFilter(
	    queryset=Sublocation.objects.all(),
	    label='Sublocation',
	    widget=ModelSelect2Widget(
	  queryset=Sublocation.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty', 'ward': 'ward'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	school_type = django_filters.ModelChoiceFilter(
		queryset = SchoolType.objects.all(),
		widget=Select2Widget
		)
	class Meta:
		model = Applicant
		fields = ['subcounty', 'ward', 'sublocation', 'school_type']
		
class LogFilter(django_filters.FilterSet):
	class Meta:
		model = HistoricalApplicant
		fields = ['history_user', 'history_type']
		labels = {
			'history_user': 'Select a user to view their logs'
		}

class DuplicatesFilter(django_filters.FilterSet):
	subcounty = django_filters.ModelChoiceFilter(
        queryset=Subcounty.objects.all(),
        widget= SubcountyWidget
    )
	ward = django_filters.ModelChoiceFilter(
	    queryset=Ward.objects.all(),
	    label='Ward',
	    widget=ModelSelect2Widget(
	  queryset=Ward.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	sublocation = django_filters.ModelChoiceFilter(
	    queryset=Sublocation.objects.all(),
	    label='Sublocation',
	    widget=ModelSelect2Widget(
	  queryset=Sublocation.objects.all(),
	    search_fields=['name__icontains'],
	    dependent_fields={'subcounty': 'subcounty', 'ward': 'ward'},
	    max_results=500,
	    attrs={'data-minimum-input-length': 0},
	)
	)
	school_type = django_filters.ModelChoiceFilter(
		queryset = SchoolType.objects.all(),
		widget=Select2Widget
		)
	class Meta:
		model = Applicant
		fields = ['first_name', 'last_name', 'subcounty', 'ward', 'sublocation', 'school_type']
		