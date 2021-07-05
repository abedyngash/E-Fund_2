from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Subcounty, Ward, Sublocation

class ApplicantResource(resources.ModelResource):
	subcounty = fields.Field(
		column_name='subcounty', 
		attribute='subcounty', 
		widget=ForeignKeyWidget(Subcounty, 'name')
		)

	ward = fields.Field(
		column_name='ward', 
		attribute='ward', 
		widget=ForeignKeyWidget(Ward, 'name')
		)

	sublocation = fields.Field(
		column_name='sublocation', 
		attribute='sublocation', 
		widget=ForeignKeyWidget(Sublocation, 'name')
		)

	class Meta:
		fields = (
			'first_name', 'last_name',
			'gender', 'school_name',
			'subcounty', 'ward', 'sublocation', 
			)