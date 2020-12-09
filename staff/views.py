from django.shortcuts import render, redirect
from django.views import View
from .forms import AddProductForm, AddBlogForm, ContactForm
from home import models as store_model
from . import models as staff_model

# Create your views here.

# ------ dashboard ------ #
class Dashboard(View):
	template_name = 'staff/dashboard/dashboard.html'
	def get(self, request):
		
		contexts = {
		}
		return render(request, self.template_name, contexts)


# ------ Product ------ #
class Product(View):
	template_name = 'staff/product/product.html'
	def get(self, request):
		products = store_model.Pharmacy.objects.all().order_by('-date')
		products_count = products.count()
		contexts = {
			'products': products,
			'products_count': products_count,
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
		form = AddProductForm(request.POST, request.FILES)
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
	def get(self, request):
		
		contexts = {
			
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

