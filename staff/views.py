from django.shortcuts import render, redirect
from django.views import View
from .forms import AddProductForm, AddBlogForm, ContactForm, EditProductForm
from home import models as store_model
from . import models as staff_model
from account import models as account_model

from django.core.paginator import Paginator
from django.http import HttpResponse

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


# ------ Product ------ #
class Product(View):
	template_name = 'staff/product/all_product.html'
	def get(self, request):
		order_by = request.GET.get('order_by')
		products = store_model.Pharmacy.objects.all().order_by(order_by.lower())

		# pagination
		paginator = Paginator(products, 4)
		page = request.GET.get('page')
		try:
			all_products = paginator.get_page(page)
		except PageNotAnInteger:
			all_products = paginator.get_page(1)
		except EmptyPage:
			all_products = paginator.get_page(paginator.num_pages)

		contexts = {
			'all_products':all_products,
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
		blogs = store_model.FoodBlog.objects.all()
		contexts = {
			'blogs':blogs,
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

