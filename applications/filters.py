from .models import Applicant, Subcounty, Ward, Sublocation, SchoolType
import django_filters
from django_select2.forms import *

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
	    widget= WardWidget
	)
	sublocation = django_filters.ModelChoiceFilter(
	    queryset=Sublocation.objects.all(),
	    widget= SublocationWidget
	)
	school_type = django_filters.ModelChoiceFilter(
		queryset = SchoolType.objects.all(),
		widget=Select2Widget
		)
	class Meta:
		model = Applicant
		fields = ['subcounty', 'ward', 'sublocation', 'school_type']
	def __init__(self, *args, **kwargs):
	    super(SchoolFilter, self).__init__(*args, **kwargs)
	    # self.filters['school_type'].label="School"

class ApplicantFilter(django_filters.FilterSet):
	subcounty = django_filters.ModelChoiceFilter(
        queryset=Subcounty.objects.all(),
        widget= SubcountyWidget
    )
	ward = django_filters.ModelChoiceFilter(
	    queryset=Ward.objects.all(),
	    widget= WardWidget
	)
	sublocation = django_filters.ModelChoiceFilter(
	    queryset=Sublocation.objects.all(),
	    widget= SublocationWidget
	)
	school_type = django_filters.ModelChoiceFilter(
		queryset = SchoolType.objects.all(),
		widget=Select2Widget
		)
	class Meta:
		model = Applicant
		fields = ['subcounty', 'ward', 'sublocation', 'school_type']
		