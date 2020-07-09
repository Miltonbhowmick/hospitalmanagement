from django.urls import path
from . import views
app_name = "home"

urlpatterns = [
	path('',views.HomeInfo.as_view(), name='home_info'),
	path('category/<str:category>/',views.CategoryDoctor.as_view(), name='category_doctor'),
	path('category/<str:category>/<str:doctor>/',views.DoctorInfo.as_view(), name='doctor'),	
	path('<str:doctor>/appointment/',views.DoctorAppointment.as_view(), name='appointment'),	
	path('labs/',views.LabDetails.as_view(), name='lab_details'),
	path('medicines/',views.PharmacyDetails.as_view(), name='pharmacy_details'),

]  