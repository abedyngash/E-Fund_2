from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from applications.models import Applicant, Subcounty, Sublocation, Ward, SchoolType
from accounting.views import get_current_financial_year, get_money_per_ward
from accounting.models import AllocationDetail
import datetime
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import modelformset_factory
from applications.forms import SchoolTypeUpdateForm

from bootstrap_modal_forms.generic import BSModalCreateView

# Create your views here.


def home(request):

	if not request.user.is_authenticated:
		context = {}
		current_year_allocation_details = AllocationDetail.objects.get(
			financial_year__start_date=datetime.date.today().year,
			financial_year__end_date=datetime.date.today().year+1
			)

		application_start_date = current_year_allocation_details.application_start_date
		application_end_date = current_year_allocation_details.application_end_date

		if application_start_date.date() < datetime.datetime.today().date() and application_end_date.date() > datetime.datetime.today().date():
			context['application_period_is_active'] = True
		else:
			context['application_period_is_active'] = False

		return render(request, 'users/dashboard/guest.html', context)

	if request.user.is_authenticated:
		if not request.user.is_entity:
			if not request.user.staffprofile.first_name:
				messages.warning(request, f'Welcome user {request.user.login_id}, please update your profile to continue')
				return redirect('profile')
		else:
			if not request.user.schoolprofile.name:
				messages.warning(request, f'Welcome user {request.user.login_id}, please update your profile to continue')
				return redirect('profile')

	if request.user.is_superuser:

		context = {
			'total_users' : User.objects.all().count(),
			'total_admins' : User.objects.all().filter(is_superuser=True).count(),
			'total_applicants' : Applicant.objects.all().count(),
			'awarded_applicants' : Applicant.objects.all().filter(award_status='awarded').count(),
			'subcounties': Subcounty.objects.all().count(),
			'wards': Ward.objects.all().count(),
			'money_per_ward' : get_money_per_ward(),
			'sublocations': Sublocation.objects.all().count(),
			'school_types': SchoolType.objects.all().count(),
			'allocation_details': AllocationDetail.objects.all().get(financial_year__start_date=datetime.date.today().year, financial_year__end_date=datetime.date.today().year+1)
		}
		return render(request, 'users/dashboard/admin.html', context)

	if request.user.is_authenticated and not request.user.is_superuser:
		if not request.user.is_entity:
			context = {
				'subcounties': Subcounty.objects.all().count(),
				'wards': Ward.objects.all().count(),
				'sublocations': Sublocation.objects.all().count(),
				'total_applicants' : Applicant.objects.all().count(),
				'awarded_applicants' : Applicant.objects.all().filter(award_status='awarded').count(),
				'allocation_details': AllocationDetail.objects.all().get(financial_year__start_date=datetime.date.today().year, financial_year__end_date=datetime.date.today().year+1),
			}
			return render(request, 'users/dashboard/staff.html', context)
		else:
			context = {
				'applicants_from_school' : Applicant.objects.all().filter(school_name=request.user.schoolprofile.name).count(),
				'reviewed_applicants': Applicant.objects.all().filter(school_name=request.user.schoolprofile.name, discipline__isnull=False).count()
			}
			return render(request, 'users/dashboard/school.html', context)

'''
End of @home method
'''

'''
@change_password method
This method is responsible for changing a user's password
'''


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/auth/password_change_form.html', {
        'form': form
    })

'''
End of @change_password method
'''

def profile(request):
	if request.user.is_entity:
		return redirect('school_profile')
	else:
		return redirect('staff_profile')

def staff_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = StaffProfileUpdateForm(request.POST, request.FILES, instance=request.user.staffprofile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('staff_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = StaffProfileUpdateForm(instance=request.user.staffprofile)

	context = {
        'u_form': u_form,
        'p_form': p_form
    }

	return render(request, 'users/profile/staff_profile.html', context)

def school_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = SchoolProfileUpdateForm(request.POST, request.FILES, instance=request.user.schoolprofile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('school_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = SchoolProfileUpdateForm(instance=request.user.schoolprofile)

	context = {
        'u_form': u_form,
        'p_form': p_form
    }

	return render(request, 'users/profile/school_profile.html', context)

@user_passes_test(lambda u: u.is_superuser)
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			login_id = form.cleaned_data.get('login_id')
			messages.success(request, f'User {login_id} registered successfully')
			return redirect('home')

	else:
		form = UserRegisterForm()

	context = {
		'title' : 'Register',
		'form' : form
	}

	return render(request, 'users/auth/register.html', context)

class SignUpView(BSModalCreateView):
    form_class = UserRegisterForm
    template_name = 'users/auth/signup.html'
    success_message = 'Success: Sign up succeeded. '
    success_url = reverse_lazy('home')

class UserListView(ListView):
	model = User
	context_object_name = 'users'

class AdminListView(ListView):
	model = User
	queryset = User.objects.all().filter(is_superuser=True)
	context_object_name = 'admins'
	template_name = 'users/admin_list.html'

# class AllocationsUpdate(SuccessMessageMixin, UpdateView):
# 	model = AllocationDetail
# 	form_class = AllocationsUpdateForm
# 	template_name = 'accounting/allocation_form.html'
# 	success_message = "Allocations Updated Successfully"
@user_passes_test(lambda u: u.is_superuser)
def AllocationsUpdate(request, id_):
	object_ = AllocationDetail.objects.get(id=id_)
	a_form = AllocationsUpdateForm(request.POST or None, instance=object_)
	SchoolTypeFormset = modelformset_factory(SchoolType, form=SchoolTypeUpdateForm, extra=0)
	formset = SchoolTypeFormset(request.POST or None)

	if a_form.is_valid():
		a_form.save()
		messages.success(request, "Allocations Updated Successfully")
		return redirect('allocation-details')

	if formset.is_valid():
		formset.save()
		messages.success(request, "Allocations Updated Successfully")
		return redirect('allocation-details')

	context = {
		'a_form': a_form,
		'formset': formset,
		'financial_year': get_current_financial_year()
	}

	return render(request, 'accounting/allocation_form.html', context)