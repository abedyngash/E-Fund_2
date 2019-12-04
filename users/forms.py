from django import forms
from .models import User, StaffProfile, SchoolProfile
from django.contrib.auth.forms import UserCreationForm
from accounting.models import AllocationDetail
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class UserRegisterForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            self.fields[field].help_text= None
        self.fields['password2'].label='CONFIRM PASSWORD'
        self.fields['password1'].label='PASSWORD'

    is_entity = forms.TypedChoiceField(
                   coerce=lambda x: x == 'True',
                   choices=((False, 'No'), (True, 'Yes')),
                   widget=forms.RadioSelect,
                   label='IS THIS A SCHOOL ENTITY?',
                   # help_text='Check this Box if the user is not a staff user'
                   )
    class Meta:
        model = User
        fields = ['login_id', 'email', 'is_entity', 'phone', 'password1', 'password2']

        labels = {
            'login_id': 'LOGIN ID',
            'email': 'EMAIL ADDRESS',
            'is_entity' : 'IS THIS A SCHOOL ENTITY?',
            'phone': 'PHONE NUMBER',
            'password2': 'CONFIRM PASSWORD'
        }

        help_texts ={
            
            'is_entity': 'Check this Box if the user is not a staff user'
        }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'email']

class UserForgotPassword(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class StaffProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['first_name', 'last_name', 'bio', 'avatar']

        widgets = {'avatar':forms.FileInput(
            attrs={'class':'form-control' }
        )}

        labels = {
            'avatar': "Change profile photo below"
        }

class SchoolProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = ['name', 'avatar']

        widgets = {'avatar':forms.FileInput(
            attrs={'class':'form-control' }
        )}

        labels = {
            'avatar': "Change profile photo below"
        }

class AllocationsUpdateForm(forms.ModelForm):
    # application_start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    # application_end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    award_period = forms.TypedChoiceField(
                   coerce=lambda x: x == 'True',
                   choices=((False, 'No'), (True, 'Yes')),
                   widget=forms.RadioSelect,
                   label='Enable Editing/Updating of Applications? (Public Participation)'
                )
    class Meta:
        model = AllocationDetail
        fields = ['amount_allocated', 'application_start_date', 'application_end_date', 'award_period']

        widgets = {
            # 'financial_year': forms.TextInput()
        }
