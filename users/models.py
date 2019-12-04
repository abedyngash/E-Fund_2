from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import reverse
from PIL import Image

from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(unique=True, max_length=70)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_entity = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null=True)
        

    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email', 'is_entity']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users' 


    def email_user(self, subject, message, from_email=None, **kwargs):
        #Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('home')


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatar.jpg',null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    def get_full_name(self):        
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):        
        return self.first_name

    def save(self, *args, **kwargs):
        super(StaffProfile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)



    def __str__(self):
        return f'{self.user.login_id}'

class SchoolProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', default='logo.png',null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.login_id}'