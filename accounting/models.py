from django.db import models
import datetime
# from applications.models import SchoolType
from django.shortcuts import reverse

YEAR_CHOICES = [(r,r) for r in range(datetime.date.today().year-1, datetime.date.today().year+30)]
# Create your models here.
class FinancialYear(models.Model):
	start_date = models.IntegerField(default=datetime.datetime.now().year)
	end_date = models.IntegerField(default=datetime.datetime.now().year+1)

	def __str__(self):
		return f'{self.start_date}/{self.end_date}'

class AllocationDetail(models.Model):
	financial_year = models.OneToOneField(FinancialYear, on_delete=models.CASCADE)
	amount_allocated = models.IntegerField()
	application_start_date = models.DateTimeField()
	application_end_date = models.DateTimeField()
	award_period = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.financial_year} {self.amount_allocated}'

	def get_absolute_url(self):
		return reverse('allocation-details')

class Cheque(models.Model):
	cheque_number = models.IntegerField()

	def __str__(self):
		return f'{self.cheque_number}'
