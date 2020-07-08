from django.contrib import admin

# Register your models here.
from .models import Category,Doctor,Appointment,Lab

admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Lab)