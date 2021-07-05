from django.urls import path, include
from .views import *

urlpatterns = [   
    path('apply', ApplicationCreateView.as_view(), name='apply'),
    path('applicants-list/', ApplicationListView.as_view(), name='applicants-list'),
    path('duplicates/', get_duplicate_applicants, name='duplicates'),
    path('applicants/<int:pk>', ApplicantDetailView.as_view(), name='applicants-detail'),
    path('applicants/<int:pk>/update', ApplicantUpdateView.as_view(), name='applicants-update'),
    path('applicants/<int:pk>/delete', ApplicantDeleteView.as_view(), name='applicants-delete'),
    path('applicants/<int:pk>/duplicate/delete', DuplicateDeleteView.as_view(), name='duplicates-delete'),
    path('awarded-applicants-list/', get_awarded_applicants, name='awarded-applicants-list'),
    path('subcounties-list/', SubcountyListView.as_view(), name='subcounties-list'),
    path('wards-list/', WardListView.as_view(), name='wards-list'),
    path('sublocations-list/', SublocationListView.as_view(), name='sublocations-list'),
    path('schooltypes-list/', SchoolTypeListView.as_view(), name='schooltypes-list'),
    path('school-applicants-list', school_applicants_view, name='school-applicants-list'),
    path('reviewed-school-applicants-list', reviewed_school_applicants_view, name='reviewed-school-applicants-list'),
    path('school-applicants-update', applicants_from_school_update, name='school-applicants-update'),

    path('logs/', ApplicantHistoryView.as_view(), name='applicants-logs'),

    path('schools/', SchoolListView.as_view(), name='schools-list'),
    path('schools/<int:pk>/update', SchoolUpdateView.as_view(), name='school-update'),
    path('schools/<int:pk>/delete', SchoolDeleteView.as_view(), name='school-delete'),

    path('export-applicants/', export_applicants_to_excel, name='export-applicants'),
    path('delete-all-applications/', delete_applications, name='delete-all-applications'),
]
