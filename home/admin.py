from django.contrib import admin

# Register your models here.
from .models import Category,Doctor,Appointment

admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Appointment)