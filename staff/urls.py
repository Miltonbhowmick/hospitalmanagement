from django.urls import path
from django.conf.urls import url
from . import views

app_name = "staff"

urlpatterns = [

	# -------- dashboard -------- #
	path('', views.Dashboard.as_view(), name='dashboard'),

	# -------- account -------- #
	path('user/<str:username>', views.UserDetailes.as_view(), name='user_details'),
	path('user-list', views.UserList.as_view(), name='user_list'),

	# -------- product --------- #	
	path('product', views.Product.as_view(), name='product'),
	path('product-add', views.AddProduct.as_view(), name='add_product'),
	path('product-edit/<str:slug>', views.EditProduct.as_view(), name='edit_product'),
	path('product-delete/<str:slug>', views.product_delete , name='delete_product'),

	# -------- Order ------------ #	
	path('order-list', views.OrderList.as_view(), name='order_list'),

	# -------- Blog ------------ #
	path('blog', views.Blog.as_view(), name='blog'),
	path('blog-add', views.AddBlog.as_view(), name='add_blog'),

	# -------- contact --------- #	
	path('contact/',views.ContactDetails.as_view(), name='contact'),

]