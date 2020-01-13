from django.urls import path
from .views import *
from users.views import AllocationsUpdate
from django.utils.text import slugify, format_lazy
from applications.views import (school_disbursements, 
								school_disbursements_details, 
								ward_disbursements, 
								ward_disbursements_details, 
								sublocation_disbursements, 
								schools_in_ward_details,								
								AddChequeForWard, 
								UpdateChequeForWard,
								AddChequeForUniOrCollege,
								UpdateChequeForUniOrCollege,
								cover_letter,
								cover_letter_for_uni_or_college,
								ward_school_types_details,
								bulk_cover_letter,
							)

urlpatterns = [
	path('', allocationdetails, name='allocation-details'),
	path('allocations/<int:id_>/update', AllocationsUpdate, name='edit-allocations'),

	path('disbursements/', disbursements_view, name='disbursements-home'),

	path('disbursements/school/', school_disbursements, name='school-disbursements'),
	path('disbursements/school/<str:school_name>/', school_disbursements_details, name='school-disbursements-details'),
	path('disbursements/ward/', ward_disbursements, name='ward-disbursements'),
	path('disbursements/ward/<int:ward_id>/', ward_disbursements_details, name='ward-disbursements-details'),
	path('disbursements/ward/<int:ward_id>/<int:school_cat_id>', ward_school_types_details, name='ward-school-types-details'),
	path('disbursements/ward/<int:ward_id>/<str:school_name>/', schools_in_ward_details, name='schools-in-ward-details'),
	path('disbursements/sublocation/', sublocation_disbursements, name='sublocation-disbursements'),

	path('ward/<int:ward_id>/school/<str:school_name>/', AddChequeForWard.as_view(), name='add-cheque-for-ward'),
	path('ward/<int:ward_id>/school/<str:school_name>/edit-cheque/<int:pk>', UpdateChequeForWard.as_view(), name='edit-cheque-for-ward'),

	path('school/<str:school_name>/<int:pk>/add_cheque', AddChequeForUniOrCollege.as_view(), name='add-cheque-for-uni-or-college'),
	path('school/edit_cheque/<str:school_name>/<int:pk>', UpdateChequeForUniOrCollege.as_view(), name='edit-cheque-for-uni-or-college'),

	path('school/<int:ward_id>/<str:school_name>/<cheque_number>/', cover_letter, name='generate-cover-letter'),
	path('school/<int:ward_id>/<int:school_cat_id>', bulk_cover_letter, name='generate-bulk-cover-letter'),
	path('school/<int:ward_id>/<str:school_name>/<cheque_number>/<int:pk>', cover_letter_for_uni_or_college, name='generate-cover-letter-for-uni-or-college')
]