from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StaffProfile, SchoolProfile
import datetime

@receiver(post_save, sender=User)
def create_staff_or_school(sender, instance, created, **kwargs):
	if created:
		if instance.is_entity:
			SchoolProfile.objects.create(user=instance)
		else:
			StaffProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_staff_or_school(sender, instance, **kwargs):
	if instance.is_entity:
		instance.schoolprofile.save()
	else:
		instance.staffprofile.save()

@receiver(user_logged_out)
def sign_user_out(sender, user, request, **kwargs):
	if request.user.is_entity:
		request.user.schoolprofile.last_logout = datetime.datetime.now()
		request.user.schoolprofile.save()
	else:
		request.user.staffprofile.last_logout = datetime.datetime.now()
		request.user.staffprofile.save()