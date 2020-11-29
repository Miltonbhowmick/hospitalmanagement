from django.shortcuts import render
from django.views import View
from .forms import ContactForm

from home import models as store_model

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
		
		contexts = {
			
		}
		return render(request, self.template_name, contexts)

class EditProduct(View):
	template_name = 'staff/product/edit_product.html'
	def get(self, request):
		
		contexts = {
			
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

