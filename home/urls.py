from django.urls import path
from . import views
app_name = "home"

urlpatterns = [
	path('',views.HomeInfo.as_view(), name='home_info'),
	path('<str:category>/',views.CategoryDoctor.as_view(), name='category_doctor'),
	path('<str:doctor>/appointment/',views.DoctorAppointment.as_view(), name='appointment'),
	path('<str:category>/<str:doctor>/',views.DoctorInfo.as_view(), name='doctor'),	
]  