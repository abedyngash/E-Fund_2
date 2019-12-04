from django.db import models
from accounting.models import FinancialYear, Cheque
from django.shortcuts import reverse
from accounting.views import get_current_financial_year

# Create your models here.
FAMILY_STATUS = (
		('orphan', 'Total Orphan'),
		('single_parent', 'Single Parent (Without Source of Income)'),
		('partial_orphan', 'Partial Orphan (Mother/Father Alive) Without Source of Income'),
		('both_parents', 'Both Parents Alive Without Source of Income'),
	)

current_financial_year = get_current_financial_year()


DISCIPLINE = (
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('poor', 'Poor'),
        ('very_poor', 'Very Poor'),
    )

GENDER = (
		('male', 'Male'),
		('female', 'Female')
)

AWARD_STATUS = (
        ('not_set' , 'Not Set'),
        ('awarded', 'Awarded'),
        ('not_awarded', 'Not Awarded'),
)

class Subcounty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
    	verbose_name_plural = "Subcounties"

    def __str__(self):
    	return self.name


class Ward(models.Model):
    subcounty = models.ForeignKey('Subcounty', related_name="wards", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
    	return self.name

class Sublocation(models.Model):
    subcounty = models.ForeignKey('Subcounty', related_name="sublocations", on_delete=models.CASCADE)
    ward = models.ForeignKey('Ward', related_name='sublocations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
    	return self.name

class SchoolType(models.Model):
    name = models.CharField(max_length=125)
    amount_allocated = models.IntegerField()

    def get_absolute_url(self):
        return reverse('allocation-details')

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(default='school@test.com')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(School, self).save(*args, **kwargs)

class Applicant(models.Model):
    # is_active = models.BooleanField(default=False)
    financial_year = models.CharField(max_length=200, default=current_financial_year)
    # financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER)
    family_status = models.CharField(max_length=200, choices=FAMILY_STATUS)

    death_cert_father = models.FileField(null=True, blank=True, upload_to='death_files/')
    death_cert_mother = models.FileField(null=True, blank=True, upload_to='death_files/')

    name_of_gurdian = models.CharField(max_length=150)
    contact_of_gurdian = models.CharField(max_length=150)
    disability_status = models.BooleanField(default=False)
    disability_desc = models.TextField(null=True, blank=True)

    school_type = models.ForeignKey(SchoolType, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=250)
    school_email = models.EmailField()
    adm_number = models.CharField(max_length=100)
    class_of_study = models.IntegerField()

    award_status = models.CharField(max_length=200, choices=AWARD_STATUS, default='not_set')
    discipline = models.CharField(max_length=250, choices=DISCIPLINE, blank=True, null=True)

    subcounty = models.ForeignKey('Subcounty', related_name="applicants", on_delete=models.CASCADE)
    ward = models.ForeignKey('Ward', related_name='applicants', on_delete=models.CASCADE)
    sublocation = models.ForeignKey('Sublocation', related_name='applicants', on_delete=models.CASCADE)

    cheque_number = models.ForeignKey(Cheque, on_delete=models.SET_NULL, null=True, blank=True) 

    @property
    def score(self):
        first_score = 0
        second_score = 0
        third_score = 0
        total_score = 0

        if self.family_status == 'orphan':
            first_score = 5
        elif self.family_status == 'single_parent':
            first_score = 4
        elif self.family_status == 'partial_orphan':
            first_score = 2
        elif self.family_status == 'both_parents':
            first_score = 1
        else:
            first_score = 0

        if self.gender == 'male':
            second_score = 2
        elif self.gender == 'female':
            second_score = 3
        else:
            second_score = 0

        if self.disability_status == True:
            third_score = 2
        elif self.disability_status == False:
            third_score = 1
        else:
            third_score = 0

        total_score = first_score + second_score + third_score

        return total_score

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.school_name = self.school_name.upper()
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.name_of_gurdian = self.name_of_gurdian.upper()

        # if self.score >= 7:
        #     self.award_status = "awarded"

        school_exists = School.objects.all().filter(name=self.school_name).exists()

        if not school_exists:            
            new_school = School.objects.create(name=self.school_name, email = self.school_email)
            new_school.save()

        super(Applicant , self).save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse('home')

