from django.shortcuts import render, redirect
from django.views import View
from .forms import AddProductForm, AddBlogForm, ContactForm, EditProductForm
from home import models as store_model
from . import models as staff_model
from account import models as account_model

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

# ------ dashboard ------ #
class Dashboard(View):
	template_name = 'staff/dashboard/dashboard.html'
	def get(self, request):
		
		# account details
		users = account_model.UserProfile.objects.filter(is_staff=False)
		total_users = users.count()
		online_users = users.filter(status=True).count()
		offline_users = total_users-online_users
		new_users = users.order_by('-id')[:4]

		# blog details
		blogs = store_model.FoodBlog.objects.all()
		total_blog = blogs.count()
		popular_blogs = store_model.FoodBlog.objects.order_by('-view')[:4]

		# product details
		products = store_model.Pharmacy.objects.all()
		total_product = products.count()
		available = products.filter(is_publish=True).count()
		unpublish = total_product-available

		contexts = {
			'total_users':total_users,
			'online_users':online_users,
			'offline_users': offline_users,
			'new_users':new_users,

			'total_blog':total_blog,
			'popular_blogs':popular_blogs,

			'total_product':total_product,
			'available':available,
			'unpublish':unpublish
		}
		return render(request, self.template_name, contexts)

# ------ User --------#
class UserList(View):
	template_name = 'staff/user/user_list.html'

	def get(self, request):
		
		order_by = request.GET.get('order_by','-date')

		users = account_model.UserProfile.objects.filter(is_staff=False).order_by(order_by.lower()).all()

		# pagination
		paginator = Paginator(users , 6)
		page = request.GET.get('page',1)
		try:
			all_users = paginator.get_page(page)
		except PageNotAnInteger:
			all_users = paginator.get_page(1)
		except EmptyPage:
			all_users = paginator.get_page(paginator.num_pages)

		contexts = {
			'all_users':all_users,
		}
		return render(request, self.template_name, contexts)

# ------ Product ------ #
class Product(View):
	template_name = 'staff/product/all_product.html'
	def get(self, request):
		direction_by = request.GET.get('dir_by','desc')
		search_by = request.GET.get('search')
		direction_column = request.GET.get('dir_col')
		order_by = request.GET.get('order_by','-date')	

		if direction_column == order_by:
			if direction_by=='asc':
				order_by = '-{}'.format(order_by)
				direction_by='desc'
			else:
				direction_by='asc'
		else:
			direction_by='asc'

		direction_column = order_by

		if search_by:
			products = store_model.Pharmacy.objects.filter( Q(name__icontains=search_by) | Q(company__name__icontains=search_by) ).order_by(order_by.lower()).all()
		else:
			products = store_model.Pharmacy.objects.order_by(order_by.lower()).all()
		
		# pagination
		paginator = Paginator(products, 4)
		page = request.GET.get('page',1)
		try:
			all_products = paginator.get_page(page)
		except PageNotAnInteger:
			all_products = paginator.get_page(1)
		except EmptyPage:
			all_products = paginator.get_page(paginator.num_pages)


		contexts = {
			'all_products':all_products,
			'order_by':order_by,
			'direction_by':direction_by,
			'direction_column':direction_column
		}
		return render(request, self.template_name, contexts)

class AddProduct(View):
	template_name = 'staff/product/add_product.html'
	def get(self, request):
		form = AddProductForm()
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)
	def post(self, request):
		form = AddProductForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			category = store_model.CategoryMedicine.objects.all()
			form.deploy()
			return redirect('staff:product')

		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

class EditProduct(View):
	template_name = 'staff/product/edit_product.html'
	def get(self, request, slug):
		product = store_model.Pharmacy.objects.get(slug=slug)
		form = EditProductForm(instance=product)
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)
	def post(self, request, slug):
		product = store_model.Pharmacy.objects.get(slug=slug)
		form = EditProductForm(request.POST or None, request.FILES or None, instance=product)

		if form.is_valid():
			product = form.deploy()
			product.save()

			return redirect('staff:product')
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ Blog -----------#
class Blog(View):
	template_name = 'staff/blog/blog.html'

	def get(self, request):

		direction_by = request.GET.get('dir_by','desc')
		direction_column = request.GET.get('dir_col')
		order_by = request.GET.get('order_by','-date')

		if direction_column==order_by:
			if direction_by == 'asc':
				order_by = '-{}'.format(order_by)
				direction_by='desc'
			else:
				direction_by='asc'
		else:
			direction_by='asc'
		direction_column = order_by
		
		blogs = store_model.FoodBlog.objects.order_by(order_by.lower()).all()

		paginator = Paginator(blogs,6)
		page = request.GET.get('page',1)
		try:
			all_blogs = paginator.get_page(page)
		except PageNotAnInteger:
			all_blogs = paginator.get_page(page)
		except EmptyPage:
			all_blogs = paginator.get_page(page)

		contexts = {
			'all_blogs':all_blogs,
			'order_by':order_by,
			'direction_by':direction_by,
			'direction_column':direction_column,
		}
		return render(request, self.template_name, contexts)

# ------ Add Blog -----------#
class AddBlog(View):
	template_name='staff/blog/add_blog.html'

	def get(self, request):
		form = AddBlogForm()
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)
	def post(self, request):
		form = AddBlogForm(request.POST, request.FILES)

		if form.is_valid():
			form.deploy()
			return redirect('staff:blog')

		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ contact ------- # 
class ContactDetails(View):
	template_name = 'staff/contact/contact.html'

	def get(self, request):
		form = ContactForm()
		contexts = {
			'form':form,
		}
		return render(request, self.template_name,contexts)
	def post(self, request):
		form = ContactForm(request.POST or None)
		if form.is_valid():
			contact = form.deploy()
			return redirect('home:home_info')
		contexts = {
			'form':form,
		}
		return render(request, self.template_name,contexts)

# ------ product delete ------- #
def product_delete(request,slug):
	store_model.Pharmacy.objects.get(slug=slug).delete()
	return redirect('staff:product')

