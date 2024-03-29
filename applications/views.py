from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import *
from .forms import ApplicationForm, SchoolTypeUpdateForm, ApplicantSchoolUpdateForm, ChequeForm, SchoolForm
from accounting.models import FinancialYear, AllocationDetail
from accounting.views import get_current_financial_year, get_money_per_ward
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.forms.models import modelformset_factory
from .filters import SchoolFilter, ApplicantFilter, LogFilter, DuplicatesFilter
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from django.db.models import Count, Sum, F, CharField
from django.db.models.functions import Concat
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.text import slugify, format_lazy
from django.template.loader import get_template
from Elimu_Fund.utils import render_to_pdf, link_callback
from xhtml2pdf import pisa
import zipfile
import io
import os
import tempfile
from django_filters.views import FilterView
from django.http import HttpRequest, HttpResponse
from .resources import ApplicantResource
# Create your views here.

class ApplicationCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
	def test_func(self):
		current_year_allocation_details = AllocationDetail.objects.get(
			financial_year__start_date=datetime.date.today().year,
			financial_year__end_date=datetime.date.today().year+1
			)
		application_start_date = current_year_allocation_details.application_start_date
		application_end_date = current_year_allocation_details.application_end_date

		if application_start_date.date() < datetime.datetime.today().date() and application_end_date.date() > datetime.datetime.today().date():
			return True
			if request.user.is_authenticated:
				return True
			return False
		return False

	def handle_no_permission(self):
		if not self.request.user.is_authenticated:
			messages.error(self.request, f'You are not authorized to access that')
			return redirect('home')
		messages.error(self.request, f'Whoops! Applications are closed for now')
		return redirect('home')

	model = Applicant
	form_class = ApplicationForm
	success_message = "Application sent successfully"
	success_url=reverse_lazy('applicants-list')

	def get_form_kwargs(self):
		kwargs = super(ApplicationCreateView, self).get_form_kwargs()
		school_list = School.objects.all().order_by('name').distinct('name')

		kwargs['data_list'] = school_list
		return kwargs

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.financial_year = get_current_financial_year()
		form.instance.family_status = 'both_parents'
		form.instance.disability_status = False
		return super(ApplicationCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
	    context = super(ApplicationCreateView, self).get_context_data(**kwargs)
	    context['title'] = 'Apply'
	    return context

class ApplicationListView(UserPassesTestMixin, FilterView):
	def test_func(self):
		if self.request.user.is_authenticated and not self.request.user.is_entity:
			return True
		return False

	def handle_no_permission(self):
		if not self.request.user.is_authenticated:
			messages.error(self.request, f'You are not authorized to access that page. Please login to access it.')
			return redirect('home')
		else:
			messages.error(self.request, f'You do not have enough priveleges to access that page.')
			return redirect('home')

	model = Applicant
	paginate_by = 1000
	filterset_class = ApplicantFilter
	template_name = 'applications/applicant_list.html'

	def get_context_data(self, **kwargs):
	    context = super(ApplicationListView, self).get_context_data(**kwargs)
	    context['total_filter'] = ApplicantFilter(self.request.GET, queryset=self.get_queryset()).qs.count()
	    context['total_applicants'] = Applicant.objects.all().count()
	    context['has_filter'] = any(field in self.request.GET for field in set(self.filterset_class.get_fields()))
	    return context
	
	def get_queryset(self):
		qs = super(ApplicationListView, self).get_queryset()
		if self.request.user.is_superuser or self.request.user.is_executive:
			return qs
		return qs.filter(user=self.request.user)

	# def get_context_data(self, **kwargs):
	#     context = super(ApplicationListView, self).get_context_data(**kwargs)
	#     # context['me'] = self.get_queryset()
	#     applicants_filter = None
	#     if self.request.user.is_superuser or self.request.user.is_executive:
	#     	applicants_filter = ApplicantFilter(self.request.GET, queryset=self.get_queryset())
	#     else:
	#     	applicants_filter = ApplicantFilter(self.request.GET, queryset=Applicant.objects.all().filter(user=self.request.user))
	    
	#     context['applicants'] = applicants_filter
	#     return context

class ApplicantDeleteView(UserPassesTestMixin, BSModalDeleteView):
	def test_func(self):
	    if self.request.user.is_superuser:
	    	return True
	    return False
	def handle_no_permission(self):
	    messages.error(self.request, "You don't have the required rights to access that")
	    return redirect('applicants-list')
	model = Applicant
	template_name = 'applications/delete_applicant.html'
	success_message = 'Success: Applicant Record was deleted.'
	success_url = reverse_lazy('applicants-list')

class DuplicateDeleteView(UserPassesTestMixin, BSModalDeleteView):
	def test_func(self):
	    if self.request.user.is_superuser:
	    	return True
	    return False
	def handle_no_permission(self):
	    messages.error(self.request, "You don't have the required rights to access that")
	    return redirect('applicants-list')
	model = Applicant
	template_name = 'applications/delete_applicant.html'
	success_message = 'Success: Duplicate Record was deleted.'
	success_url = reverse_lazy('duplicates')

def get_awarded_applicants(request):
	awarded_applicants = Applicant.objects.filter(award_status="awarded")
	applicants_filter = ApplicantFilter(request.GET, queryset=awarded_applicants)
	context = {
		'awarded_applicants' : applicants_filter
	}
	return render(request, 'applications/awarded_applicants.html', context)

class ApplicantUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Applicant
	form_class = ApplicationForm
	template_name = 'applications/update_applicant_form.html'
	success_url =reverse_lazy('applicants-list')
	success_message = "Record Updated Successfully"

	def test_func(self):
		if self.request.user.is_authenticated:
			return True
		return False

	def handle_no_permission(self):
		messages.error(self.request, f'You are not authorized to access that.')
		return redirect('home')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ApplicantUpdateView, self).form_valid(form)


	def get_context_data(self, **kwargs):
	    context = super(ApplicantUpdateView, self).get_context_data(**kwargs)
	    context['title'] = "Edit Application Details"
	    context['money_per_ward'] = get_money_per_ward()
	    current_ward = self.get_object().ward
	    current_sublocation = self.get_object().sublocation
	    amount_so_far = Applicant.objects.filter(ward=current_ward, sublocation=current_sublocation, award_status='awarded').aggregate(total=Sum('school_type__amount_allocated'))
	    # print(total_price['total'])
	    context['amount_so_far'] = amount_so_far
	    context['sublocations_count'] = Sublocation.objects.all().filter(ward=current_ward).count()
	    return context

	def get_form_kwargs(self):
		kwargs = super(ApplicantUpdateView, self).get_form_kwargs()
		school_list = School.objects.all().order_by('name').distinct('name')

		kwargs['data_list'] = school_list
		return kwargs

class ApplicantUpdateViewFromDisbursements(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Applicant
	form_class = ApplicationForm
	template_name = 'applications/update_applicant_form.html'
	# success_url =reverse_lazy('')
	success_message = "Record Updated Successfully"

	def get_success_url(self, **kwargs):
		return reverse_lazy('applicants-from-ward', kwargs={'ward_id': self.get_object().ward_id})

	def test_func(self):
		if self.request.user.is_authenticated:
			return True
		return False

	def handle_no_permission(self):
		messages.error(self.request, f'You are not authorized to access that.')
		return redirect('home')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ApplicantUpdateViewFromDisbursements, self).form_valid(form)


	def get_context_data(self, **kwargs):
	    context = super(ApplicantUpdateViewFromDisbursements, self).get_context_data(**kwargs)
	    context['title'] = "Edit Application Details"
	    context['money_per_ward'] = get_money_per_ward()
	    current_ward = self.get_object().ward
	    current_sublocation = self.get_object().sublocation
	    amount_so_far = Applicant.objects.filter(ward=current_ward, sublocation=current_sublocation, award_status='awarded').aggregate(total=Sum('school_type__amount_allocated'))
	    # print(total_price['total'])
	    context['amount_so_far'] = amount_so_far
	    context['sublocations_count'] = Sublocation.objects.all().filter(ward=current_ward).count()
	    return context

	def get_form_kwargs(self):
		kwargs = super(ApplicantUpdateViewFromDisbursements, self).get_form_kwargs()
		school_list = School.objects.all().order_by('name').distinct('name')

		kwargs['data_list'] = school_list
		return kwargs


class ApplicantDetailView(BSModalReadView):
    model = Applicant

def get_duplicate_applicants(request):
	school_names = Applicant.objects.values('school_name').annotate(Count('id')).order_by().filter(id__count__gt=1)
	qs = Applicant.objects.annotate(
            dupe_id=Concat(
                        F('first_name')
                        , F('last_name')
                        , F('school_name')
                        , output_field=CharField()
            )
        ).order_by('first_name', 'last_name')

	dupes = qs.values('dupe_id').annotate(dupe_count=Count('dupe_id')).filter(dupe_count__gt=1)
	dupe_keys = []
	for dupe in dupes:
		dupe_keys.append(dupe['dupe_id'])

	# applicants_filter = DuplicatesFilter(request.GET, queryset=duplicate_records)

	context = {
		'duplicate_records': qs,
		'dupe_keys': dupe_keys,
	}

	return render(request, 'applications/duplicate_records.html', context)

class SubcountyListView(ListView):
	model = Subcounty
	context_object_name = 'subcounties'

class WardListView(ListView):
	model = Ward
	context_object_name = 'wards'

class SublocationListView(ListView):
	model = Sublocation
	context_object_name = 'sublocations'

class SchoolTypeListView(ListView):
	model = SchoolType
	context_object_name = 'schooltypes'

def school_applicants_view(request):
	applicants_from_school = Applicant.objects.all().filter(school_name=request.user.schoolprofile.name)

	context = {
		'applicants_from_school': applicants_from_school,
	}

	return render(request, 'applications/school_applicants.html', context)

def reviewed_school_applicants_view(request):
	applicants_from_school = Applicant.objects.all().filter(school_name=request.user.schoolprofile.name).exclude(discipline__isnull=True).exclude(discipline__exact='')

	context = {
		'applicants_from_school': applicants_from_school,
	}

	return render(request, 'applications/reviewed_school_applicants.html', context)

def applicants_from_school_update(request):
	ApplicantsFormset = modelformset_factory(Applicant, form=ApplicantSchoolUpdateForm, extra=0)
	formset = ApplicantsFormset(request.POST or None, queryset=Applicant.objects.filter(school_name=request.user.schoolprofile.name))

	if formset.is_valid():
		instances = formset.save(commit=False)
		for instance in instances:
			instance.save()
			
		messages.success(request, "Applicant reviewed successfully")
		return redirect('school-applicants-list')

	context = {
		'formset' : formset
	}

	return render(request, 'applications/school_applicant_form.html', context)

def school_disbursements(request):
	schools = Applicant.objects.all().filter(award_status='awarded').values('school_name', 'cheque_number__cheque_number','cheque_number__id','school_type').order_by('school_name').annotate(name_count=Count('school_name'))
	school_filter = SchoolFilter(request.GET, queryset=schools)
	context = {
		'title': 'School Disbursements',
		# 'schools' : schools,
		'filter': school_filter,
	}
	return render(request, 'accounting/disbursements/school_disbursements/school_disbursements.html', context)

def school_disbursements_details(request, school_name):
	school_applicants = Applicant.objects.filter(school_name=school_name, award_status='awarded')
	cheque_number = school_applicants.values_list('cheque_number__cheque_number', flat=True).distinct()
	uni_or_college = Applicant.objects.filter(school_name=school_name, award_status="awarded", school_type__name__in=['University', 'College'])
	total_amount = Applicant.objects.filter(school_name=school_name, award_status='awarded').aggregate(total=Sum('school_type__amount_allocated'))

	context = {
		'school_name': school_name,
		'cheque_number': cheque_number,
		'applicants': school_applicants,
		'total_amount': total_amount,
		'uni_or_college': uni_or_college
	}

	return render(request, 'accounting/disbursements/school_disbursements/school_disbursement_details.html', context)

def ward_disbursements(request):
	ward_applicants = Ward.objects.all().filter(applicants__award_status='awarded').annotate(no_of_sublocations=Count('sublocations', 
									distinct=True)).annotate(no_of_applicants=Count('applicants', 
									distinct=True))

	context = {
		'ward_applicants' : ward_applicants,
		'money_per_ward': get_money_per_ward(),
	}

	return render(request, 'accounting/disbursements/ward_disbursements/ward_disbursements.html', context)

def ward_disbursements_details(request, ward_id):
	schooltypes = SchoolType.objects.all()
	ward = Ward.objects.get(id=ward_id)
	amount_so_far = Applicant.objects.all().filter(ward_id=ward_id).aggregate(amount=Sum('school_type__amount_allocated'))
	money_per_ward = get_money_per_ward()
	amount_remaining = money_per_ward - amount_so_far['amount']
	context = {
		# 'schools': schools_with_applicants,
		'amount_so_far': amount_so_far['amount'],
		'amount_remaining': amount_remaining,
		'school_types' : schooltypes,
		'ward': ward,
	}

	return render(request, 'accounting/disbursements/ward_disbursements/ward_school_types.html', context)

def ward_school_types_details(request, ward_id, school_cat_id):
	if school_cat_id == 1:
		applicants_in_university = Applicant.objects.all().filter(
				award_status="awarded", ward_id=ward_id, school_type_id=school_cat_id
			).order_by('cheque_number__cheque_number', 'school_name').annotate(total=Sum('school_type__amount_allocated'))
		school_filter = SchoolFilter(request.GET, queryset=applicants_in_university)
		ward = Ward.objects.get(id=ward_id)
		school_type = SchoolType.objects.get(id=school_cat_id)
		cheque_number = applicants_in_university.values_list('cheque_number__cheque_number', flat=True).distinct()

		context = {
			# 'schools': schools_with_applicants,
			'filter' : school_filter,
			'ward': ward,
			'school_type': school_type,
			'cheque_number': cheque_number
		}

		return render(request, 'accounting/disbursements/ward_disbursements/university_ward_disbursements_details.html', context)

	else:
		schools_in_category = Applicant.objects.all().filter(
				award_status="awarded", ward_id=ward_id, school_type_id=school_cat_id
			).order_by('cheque_number__cheque_number', 'school_name').values('school_name', 'ward_id', 'school_type', 'cheque_number', 'cheque_number__cheque_number','cheque_number__id').annotate(
			name_count=Count('school_name'), total=Sum('school_type__amount_allocated'))

		school_filter = SchoolFilter(request.GET, queryset=schools_in_category)
		ward = Ward.objects.get(id=ward_id)
		school_type = SchoolType.objects.get(id=school_cat_id)
		cheque_number = schools_in_category.values_list('cheque_number__cheque_number', flat=True).distinct()

		context = {
			# 'schools': schools_with_applicants,
			'filter' : school_filter,
			'ward': ward,
			'school_type': school_type,
			'cheque_number': cheque_number
		}

		return render(request, 'accounting/disbursements/ward_disbursements/ward_disbursements_details.html', context)

def bulk_cover_letter(request, ward_id, school_cat_id):
	school_type = SchoolType.objects.get(id=school_cat_id)
	ward = Ward.objects.get(id=ward_id)

	if school_cat_id == 1:
		applicants_in_university = Applicant.objects.filter(school_type=school_type, ward_id=ward_id, award_status='awarded').order_by('cheque_number__cheque_number', 'school_name')
		context = {
			'applicants_in_university' : applicants_in_university,
			# 'beneficiaries' : beneficiaries,
			'ward': ward,
			'school_type': school_type,
		}

		response = HttpResponse('<title>Cover Letter</title>', content_type='application/pdf')
		filename = "%s_%s.pdf" %(ward, school_type)
		content = "inline; filename=%s" %(filename)
		response['Content-Disposition'] = content
		template = get_template('university_cover_letter_bulk.html')
		html = template.render(context)
		pdf = pisa.CreatePDF(
	   		html, dest=response, link_callback=link_callback)
		return response
	else:
		schools_in_school_type = Applicant.objects.filter(school_type=school_type, ward_id=ward_id, award_status='awarded').order_by('cheque_number__cheque_number', 'school_name').values_list('school_name', flat=True).distinct()
		cheque_number = Applicant.objects.filter(school_type=school_type, ward_id=ward_id, award_status='awarded').values_list('cheque_number__cheque_number', flat=True).distinct()
		beneficiaries = Applicant.objects.filter(school_type=school_type, ward_id=ward_id, award_status='awarded')


		context = {
			'schools_in_school_type' : schools_in_school_type,
			'beneficiaries' : beneficiaries,
			'ward': ward,
			'school_type': school_type,
		}

		response = HttpResponse('<title>Cover Letter</title>', content_type='application/pdf')
		filename = "%s_%s.pdf" %(ward, school_type)
		content = "inline; filename=%s" %(filename)
		response['Content-Disposition'] = content
		template = get_template('cover_letter_bulk.html')
		html = template.render(context)
		pdf = pisa.CreatePDF(
	   		html, dest=response, link_callback=link_callback)
		return response

def schools_in_ward_details(request, ward_id, school_cat_id, school_name):
	school_applicants = Applicant.objects.filter(school_name=school_name, ward_id=ward_id, award_status='awarded')
	total_amount = Applicant.objects.filter(school_name=school_name, ward_id=ward_id, award_status='awarded').aggregate(total=Sum('school_type__amount_allocated'))
	ward = Ward.objects.get(id=ward_id)
	school_type = SchoolType.objects.get(id=school_cat_id)
	uni_or_college = Applicant.objects.filter(school_name=school_name, award_status="awarded", school_type__name__in=['University', 'College'])
	cheque_number = school_applicants.values_list('cheque_number__cheque_number', flat=True).distinct()

	context = {
		'school_name': school_name,
		'applicants': school_applicants,
		'total_amount': total_amount,
		'ward' : ward,
		'school_type': school_type,
		'uni_or_college' : uni_or_college,
		'cheque_number': cheque_number
	}

	return render(request, 'accounting/disbursements/ward_disbursements/schools_in_ward_details.html', context)

def sublocation_disbursements(request):
	context = {}
	context['wards'] = Ward.objects.all()

	if request.GET.get('wards_select'):
		wards_filter = request.GET.get('wards_select')
		current_ward = Ward.objects.filter(id=wards_filter).values()
		context['selected_ward'] = Ward.objects.get(id=wards_filter)


		for value in current_ward:
			request.session['current_ward'] = value['name']
			

		context['sublocations'] = Sublocation.objects.all().filter(
			ward=wards_filter, applicants__award_status='awarded').annotate(
			no_of_applicants=Count('applicants')).annotate(total=Sum(
				'applicants__school_type__amount_allocated'))
		context['sublocation_count'] = Sublocation.objects.all().filter(ward=wards_filter).count()
	else:
		try:
			del request.session['current_ward']
		except KeyError:
			pass
	context['money_per_ward'] = get_money_per_ward()
	return render(request, 'accounting/disbursements/sublocation_disbursements/sublocation_disbursements.html', context)

class AddChequeForWard(BSModalCreateView):
	form_class = ChequeForm
	template_name = 'accounting/add_cheque_form.html'
	success_message = 'Success: Cheque Added'
	# success_url = reverse_lazy('ward-school-types-details')

	def get_success_url(self):
		ward_id = self.kwargs['ward_id']
		school_cat_id = self.kwargs['school_cat_id']
		return reverse('ward-school-types-details', kwargs={'ward_id': ward_id, 'school_cat_id':school_cat_id })

	def form_valid(self, form):

		ward_id = self.kwargs['ward_id']
		school_name = self.kwargs['school_name']
		school_cat_id = self.kwargs['school_cat_id']

		instance = form.save()
		instance.save()

		cheque_beneficiaries = Applicant.objects.filter(school_name=school_name, school_type_id=school_cat_id, ward_id=ward_id, award_status='awarded')
		cheque_beneficiaries.update(cheque_number=instance)
		return super(AddChequeForWard, self).form_valid(form)

class AddChequeForUniOrCollege(BSModalCreateView):
	form_class = ChequeForm
	template_name = 'accounting/add_cheque_form.html'
	success_message = 'Success: Cheque Number Added'
	# success_url = reverse_lazy('school-disbursements')
	extra_content = {'title': 'Add Cheque'}

	def get_success_url(self):
		ward_id = self.kwargs['ward_id']
		school_cat_id = self.kwargs['school_cat_id']
		return reverse('ward-school-types-details', kwargs={'ward_id': ward_id, 'school_cat_id':school_cat_id })

	def form_valid(self, form):
		pk = self.kwargs['pk']
		instance = form.save()
		instance.save()

		applicant = Applicant.objects.filter(pk=pk)
		applicant.update(cheque_number=instance)

		return super(AddChequeForUniOrCollege, self).form_valid(form)

class UpdateChequeForWard(BSModalUpdateView):
	model = Cheque
	template_name = 'accounting/edit_cheque_form.html'
	form_class = ChequeForm
	success_message = 'Success: Cheque was updated.'
	# success_url = reverse_lazy('ward-disbursements')
	extra_content = {'title': 'Edit Cheque'}

	def get_success_url(self):
		ward_id = self.kwargs['ward_id']
		school_cat_id = self.kwargs['school_cat_id']
		return reverse('ward-school-types-details', kwargs={'ward_id': ward_id, 'school_cat_id':school_cat_id })

	def form_valid(self, form):
		ward_id = self.kwargs['ward_id']
		school_cat_id = self.kwargs['school_cat_id']
		school_name = self.kwargs['school_name']

		instance = form.save()
		instance.save()

		cheque_beneficiaries = Applicant.objects.filter(school_name=school_name, school_type_id=school_cat_id, ward_id=ward_id, award_status='awarded')
		cheque_beneficiaries.update(cheque_number=instance)
		return super(UpdateChequeForWard, self).form_valid(form)

class UpdateChequeForUniOrCollege(BSModalUpdateView):
	model = Cheque
	template_name = 'accounting/edit_cheque_form.html'
	form_class = ChequeForm
	success_message = 'Success: Cheque was updated.'
	success_url = reverse_lazy('school-disbursements')
	extra_content = {'title': 'Edit Cheque'}

	def get_success_url(self):
		ward_id = self.kwargs['ward_id']
		school_cat_id = self.kwargs['school_cat_id']
		return reverse('ward-school-types-details', kwargs={'ward_id': ward_id, 'school_cat_id':school_cat_id })

	def form_valid(self, form):
		instance = form.save()
		instance.save()
		self.object.applicant_set.update(cheque_number=instance)
		return super(UpdateChequeForUniOrCollege, self).form_valid(form)

def cover_letter(request, ward_id, school_name, cheque_number):
	# print(cheque_number)
	if cheque_number == None:
		return redirect('home')

	beneficiaries = Applicant.objects.filter(school_name=school_name, ward_id=ward_id, award_status="awarded")
	total_amount_to_beneficiaries = Applicant.objects.filter(school_name=school_name, ward_id=ward_id, award_status="awarded").aggregate(total=Sum('school_type__amount_allocated'))
	
	context = {
		'school_name' : school_name,
		'beneficiaries' : beneficiaries,
		'total_amount_to_beneficiaries' : total_amount_to_beneficiaries,
		'title' : school_name + ' Disbursement Details',
		'cheque_number': cheque_number
	}


	
	response = HttpResponse('<title>Cover Letter</title>', content_type='application/pdf')
	filename = "%s.pdf" %(cheque_number)
	content = "inline; filename=%s" %(filename)
	response['Content-Disposition'] = content
	template = get_template('cover_letter.html')
	html = template.render(context)
	pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)

	return response

def cover_letter_for_uni_or_college(request, school_name, ward_id, cheque_number, pk):
	object_ = get_object_or_404(Applicant, pk=pk)
	
	total_amount_to_beneficiaries = Applicant.objects.filter(id=pk, ward_id=ward_id,award_status="awarded").aggregate(total=Sum('school_type__amount_allocated'))
	context = {
		'object' : object_,
		'total_amount_to_beneficiaries' : total_amount_to_beneficiaries,
		'cheque_number': cheque_number,
	}

	response = HttpResponse('<title>Cover Letter</title>', content_type='application/pdf')
	filename = "%s.pdf" %(cheque_number)
	content = "inline; filename=%s" %(filename)
	response['Content-Disposition'] = content
	template = get_template('cover_letter.html')
	html = template.render(context)
	pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback
       )

	return response

class ApplicantHistoryView(FilterView):
	template_name = "applications/applicant_history_list.html"
	paginate_by = 200
	filterset_class = LogFilter

	def get_queryset(self):
		history = Applicant.history.all()
		return history

	def get_context_data(self, **kwargs):
	    context = super(ApplicantHistoryView, self).get_context_data(**kwargs)
	    context['total_filter'] = LogFilter(self.request.GET, queryset=self.get_queryset()).qs.count()
	    context['total_records'] = Applicant.history.all().count()
	    context['has_filter'] = any(field in self.request.GET for field in set(self.filterset_class.get_fields()))
	    return context

	# def get_context_data(self, **kwargs):
	#     context = super(ApplicantHistoryView, self).get_context_data(**kwargs)
	#     logs = Applicant.history.all()
	#     logs_filter = LogFilter(self.request.GET, queryset=logs)
	#     context['logs'] = logs_filter
	#     return context

class SchoolListView(ListView):
	model = School
	context_object_name = 'schools'
	queryset = School.objects.all().order_by('name').distinct('name')

class SchoolUpdateView(BSModalUpdateView):
	model = School
	template_name = 'applications/edit_school_form.html'
	form_class = SchoolForm
	success_message = 'Success: School was updated.'
	success_url = reverse_lazy('schools-list')
	extra_content = {'title': 'Edit School'}

class SchoolDeleteView(UserPassesTestMixin, BSModalDeleteView):
	def test_func(self):
	    if self.request.user.is_superuser:
	    	return True
	    return False
	def handle_no_permission(self):
	    messages.error(self.request, "You don't have the required rights to access that")
	    return redirect('schools-list')
	model = School
	template_name = 'applications/delete_school.html'
	success_message = 'Success: SCHOOL was deleted.'
	success_url = reverse_lazy('applicants-list')


def get_applicants_per_ward(request, ward_id):
	applicants = Applicant.objects.all().filter(ward_id=ward_id)
	total_amount_allocated = Applicant.objects.all().filter(ward_id=ward_id).aggregate(total=Sum('school_type__amount_allocated'))
	context = {
		'applicants': applicants,
		'total_amount': total_amount_allocated,
		'ward': Ward.objects.get(id=ward_id)
	}

	return render(request, 'accounting/disbursements/ward_disbursements/applicants_from_ward.html', context)

def export_applicants_to_excel(request: HttpRequest) -> HttpResponse:
	applicants = Applicant.objects.all()
	data = ApplicantResource().export(applicants).csv
	response = HttpResponse(data, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=export.csv'
	return response

def delete_applications(request):
	total_applicants = Applicant.objects.all().count()
	if request.method == 'POST':		
		Applicant.objects.all().delete()
		messages.success(request, f'{total_applicants} applicants deleted successfully')
		return redirect('applicants-list')
	return render(request, 'applications/applications_delete_confirm.html', {'total_applicants': total_applicants})