from django.contrib import admin
from imagekit.admin import AdminThumbnail
# Register your models here.
from .models import Category,Doctor,Appointment,Lab, Pharmacy, MedicineCompany, CategoryMedicine, FoodBlog, Contact

class AppointmentAdmin(admin.ModelAdmin):
	search_fields = ['email',]

admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Lab)
admin.site.register(Pharmacy)
admin.site.register(MedicineCompany)
admin.site.register(CategoryMedicine)
admin.site.register(FoodBlog)
admin.site.register(Contact)