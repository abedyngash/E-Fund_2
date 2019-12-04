from applications import models as applications_models
import django_filters

class SchoolFilter(django_filters.FilterSet):
	class Meta:
		model = applications_models.Applicant
		fields = ['school_type']