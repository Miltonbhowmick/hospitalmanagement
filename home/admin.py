from django.contrib import admin
from imagekit.admin import AdminThumbnail
# Register your models here.
from . import models

class AppointmentAdmin(admin.ModelAdmin):
	search_fields = ['email',]

admin.site.register(models.Category)
admin.site.register(models.Doctor)
admin.site.register(models.Appointment, AppointmentAdmin)
admin.site.register(models.Lab)
admin.site.register(models.Pharmacy)
admin.site.register(models.MedicineCompany)
admin.site.register(models.CategoryMedicine)
admin.site.register(models.FoodBlog)