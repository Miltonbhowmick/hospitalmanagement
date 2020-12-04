from django.urls import path
from . import views
app_name = "home"

urlpatterns = [
	path('',views.HomeInfo.as_view(), name='home_info'),

	# ------- Doctor --------- # 
	path('category/<str:category>/',views.CategoryDoctor.as_view(), name='category_doctor'),
	path('category/<str:category>/<str:doctor>/',views.DoctorInfo.as_view(), name='doctor'),	
	path('<str:doctor>/appointment/',views.DoctorAppointment.as_view(), name='appointment'),	

	# ------- Lab --------- # 
	path('labs/',views.LabDetails.as_view(), name='lab_details'),

	# ------- Product --------- # 
	path('<str:med_category>/medicines/',views.CategoryMedicineDetails.as_view(), name='category_medicine_details'),
	path('pharmacy/',views.PharmacyDetails.as_view(), name='pharmacy_details'),
	path('pharmacy/medicines/<str:slug>',views.MedicineDetails.as_view(), name='medicine_details'),

	# ------- Cart --------- # 
	path('update-cart/', views.update_cart, name='update_cart'),
	path('cart/', views.CartDetails.as_view(), name='cart_details'),

	# ------- Checkout --------- # 
	path('checkout/', views.Checkout.as_view(), name='checkout'),

	# ------- Blog --------- # 
	path('food/posts/',views.FoodBlogDetails.as_view(), name='food_posts'),
	path('food/search/',views.FoodBlogSearch.as_view(), name='food_blog_search'),
	path('food/<str:slug>/',views.FoodBlogPost.as_view(), name='food_blog_post'),

	#--------- PAYMENT ----------#
	path('charge/', views.charge, name='charge'),
	path('success/<str:args>/', views.success, name='success'),
]  