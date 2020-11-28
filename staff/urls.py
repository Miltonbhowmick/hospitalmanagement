from django.urls import path
from django.conf.urls import url
from . import views

app_name = "staff"

urlpatterns = [

	path('', views.Dashboard.as_view(), name='dashboard'),
	path('contact/',views.ContactDetails.as_view(), name='contact'),
	
]