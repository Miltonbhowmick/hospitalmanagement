from django.contrib import admin

# Register your models here.
from .models import Category,Doctor,Appointment,Lab, Pharmacy,MedicineCompany, CategoryMedicine, FoodBlog

admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Lab)
admin.site.register(Pharmacy)
admin.site.register(MedicineCompany)
admin.site.register(CategoryMedicine)
admin.site.register(FoodBlog)