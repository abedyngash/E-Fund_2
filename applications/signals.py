from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Applicant, School

@receiver(pre_save, sender=School)
def check_names(sender, instance, **kwargs):
	if not instance._state.adding:
		new_name = instance.name
		old_name = School.objects.get(pk=instance.id)
		if old_name:
			Applicant.objects.filter(school_name=old_name).update(school_name=new_name)

@receiver(post_save, sender=Applicant)
def create_school(sender, instance, created, **kwargs):
	school_name_exists = Applicant.objects.all().filter(school_name=instance.school_name).exists()
	if created:
		if not school_name_exists:
			new_school = School.objects.create(name=instance.school_name)
			new_school.save()



@receiver(post_save, sender=Applicant)
def save_school(sender, instance, **kwargs):
	school_name_exists = Applicant.objects.all().filter(school_name=instance.school_name).exists()
	if not school_name_exists:
		School.objects.save(name=instance.school_name)
