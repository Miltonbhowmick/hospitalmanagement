from django.contrib import admin
from .models import UserProfile, Staff
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Staff)