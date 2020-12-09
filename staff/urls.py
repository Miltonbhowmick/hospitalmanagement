from django.urls import path
from django.conf.urls import url
from . import views

app_name = "staff"

urlpatterns = [

	# -------- dashboard -------- #
	path('', views.Dashboard.as_view(), name='dashboard'),

	# -------- product --------- #	
	path('product', views.Product.as_view(), name='product'),
	path('product-add', views.AddProduct.as_view(), name='add_product'),
	path('product-<int:id>', views.EditProduct.as_view(), name='edit_product'),

	# -------- Blog ------------ #
	path('blog', views.Blog.as_view(), name='blog'),
	path('blog-add', views.AddBlog.as_view(), name='add_blog'),

	# -------- contact --------- #	
	path('contact/',views.ContactDetails.as_view(), name='contact'),

]