from django import forms
from .models import *
from django_select2.forms import *
from.fields import ListTextWidget
from accounting.models import Cheque, AllocationDetail
from bootstrap_modal_forms.forms import BSModalForm
import datetime

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


class ApplicationForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    # award_period_is_active = getattr(
    #   AllocationDetail.objects.get(
    #   financial_year__start_date=datetime.date.today().year,
    #   financial_year__end_date=datetime.date.today().year+1
    #   ), 
    #   'award_period')
    _school_list = kwargs.pop('data_list', None)
    super(ApplicationForm, self).__init__(*args, **kwargs)
    self.fields['school_name'].widget = ListTextWidget(data_list=_school_list, name='school-list')
    # if not award_period_is_active:
    #   self.fields['award_status'].widget = forms.HiddenInput()

  class Meta:
    model = Applicant

    fields = [
    # 'award_status',
    'first_name', 'last_name', 'gender', 
    'name_of_gurdian', 'contact_of_gurdian',
    'school_type', 'school_name', 'adm_number', 'class_of_study',
    'subcounty', 'ward', 'sublocation'
    ]

    widgets = {
      'subcounty': SubcountyWidget,
      'ward': WardWidget,
      'sublocation': SublocationWidget,
    }

    help_texts = {
    }

    labels ={
    }

class SchoolTypeUpdateForm(forms.ModelForm):
  class Meta:
    model = SchoolType
    fields = ['name', 'amount_allocated']
    widgets = {
      'name' : forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': 'true'})
    }

class ApplicantSchoolUpdateForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
      super(ApplicantSchoolUpdateForm, self).__init__(*args, **kwargs)
      self.fields['first_name'].widget.attrs['readonly'] = True
      self.fields['last_name'].widget.attrs['readonly'] = True
  class Meta:
    model = Applicant
    fields = [
    'first_name', 'last_name', 'discipline'
    ]

    # widgets = {
    #   'first_name': forms.TextInput(attrs={'class': 'col-md-4 form-control'}),
    #   'last_name': forms.TextInput(attrs={'class': 'col-md-4 form-control'}),
    #   'discipline': forms.TextInput(attrs={'class': 'col-md-4 form-control'}),
    # }

class ChequeForm(BSModalForm):
  class Meta:
    model = Cheque
    fields = ['cheque_number']

class SchoolForm(BSModalForm):
  class Meta:
    model = School
    fields = ['name']
