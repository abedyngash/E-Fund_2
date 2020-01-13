from django.urls import path, include
from .views import *

urlpatterns = [   
    path('apply', ApplicationCreateView.as_view(), name='apply'),
    path('applicants-list/', ApplicationListView.as_view(), name='applicants-list'),
    path('applicants/<int:pk>', ApplicantDetailView.as_view(), name='applicants-detail'),
    path('applicants/<int:pk>/update', ApplicantUpdateView.as_view(), name='applicants-update'),
    path('awarded-applicants-list/', get_awarded_applicants, name='awarded-applicants-list'),
    path('subcounties-list/', SubcountyListView.as_view(), name='subcounties-list'),
    path('wards-list/', WardListView.as_view(), name='wards-list'),
    path('sublocations-list/', SublocationListView.as_view(), name='sublocations-list'),
    path('schooltypes-list/', SchoolTypeListView.as_view(), name='schooltypes-list'),
    path('school-applicants-list', school_applicants_view, name='school-applicants-list'),
    path('reviewed-school-applicants-list', reviewed_school_applicants_view, name='reviewed-school-applicants-list'),
    path('school-applicants-update', applicants_from_school_update, name='school-applicants-update'),

    path('logs/', ApplicantHistoryView.as_view(), name='applicants-logs')
]