from django.urls import path
from . import views
app_name = "home"

urlpatterns = [
	path('',views.HomeInfo.as_view(), name='home_info'),
	path('category/<str:category>/',views.CategoryDoctor.as_view(), name='category_doctor'),
	path('category/<str:category>/<str:doctor>/',views.DoctorInfo.as_view(), name='doctor'),	
	path('<str:doctor>/appointment/',views.DoctorAppointment.as_view(), name='appointment'),	
	path('labs/',views.LabDetails.as_view(), name='lab_details'),
	path('<str:med_category>/medicines/',views.CategoryMedicineDetails.as_view(), name='category_medicine_details'),
	path('pharmacy/',views.PharmacyDetails.as_view(), name='pharmacy_details'),
	path('pharmacy/medicines/<str:slug>',views.MedicineDetails.as_view(), name='medicine_details'),
	path('food/posts/',views.FoodBlogDetails.as_view(), name='food_posts'),
	path('food/search/',views.FoodBlogSearch.as_view(), name='food_blog_search'),
	path('food/<str:slug>/',views.FoodBlogPost.as_view(), name='food_blog_post'),
	path('contact/',views.ContactDetails.as_view(), name='contact'),	
]  