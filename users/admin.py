from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SchoolProfile)
admin.site.register(StaffProfile)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ['login_id', 'email']
	search_fields = ['login_id', 'email']