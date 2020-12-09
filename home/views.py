from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
# Create your views here.
from account.models import UserProfile
from .models import Doctor,Category,Appointment,Lab, MedicineCompany, Pharmacy, CategoryMedicine, FoodBlog
from sell.models import Cart, Order, OrderStatus
from .forms import AppointmentForm
from django.core.mail import send_mail
from django.db.models import Q
import json
import datetime

import stripe
stripe.api_key = "sk_test_gb8wU1OGozJ4L5Zs14e1JRka00pdcIDlPD"


#------- Home -------#
class HomeInfo(View):
	template_name = 'home/home.html'
	def get(self, request):
		doctors = Doctor.objects.all()
		categories = Category.objects.all()
		appointments = Appointment.objects.all()
		urgent_resolve = Appointment.objects.filter(Q(urgent_resolve=True) & Q(complete=True)).count()

		users = UserProfile.objects.all()
		
		context = {
			'appointments':appointments,
			'doctors':doctors,
			'categories': categories,	
			'urgent_resolve':urgent_resolve,		
			'users':users,
		}

		return render(request,self.template_name,context)

#------- Doctors of Category  -------#
class CategoryDoctor(View):
	template_name = 'home/doctor_details.html'

	def get(self, request, category):
		doctors = Doctor.objects.filter(doctor_category__slug=category)
		category = Category.objects.get(slug=category)
		context = {
			'category':category,
			'doctors':doctors,
		}
		if doctors:
			return render(request, self.template_name,context)
		else:
			return HttpResponse('No doctors')

#------- Doctor Info -------#
class DoctorInfo(View):
	template_name = 'home/doctor_info_details.html'

	def get(self, request,category, doctor):
		doctor = Doctor.objects.get(slug=doctor)
		context = {
			'doctor':doctor,
		}
		return render(request, self.template_name,context)

#------- Appointment -------#
class DoctorAppointment(View):
	template_name = 'home/appointment.html'
	def get(self, request,doctor):
		doctor = Doctor.objects.get(slug=doctor)
		form = AppointmentForm()
		context = {
			'form':form,
			'doctor':doctor,
		}
		return render(request, self.template_name,context)

	def post(self, request, doctor):
		doctor = Doctor.objects.get(slug=doctor)
		form = AppointmentForm(request.POST or None)
		print(form.errors)

		if form.is_valid():
			appointment = form.deploy()
			appointment.doctor=doctor
			if request.user.is_authenticated:
				appointment.user = request.user
			appointment.save()
		
			date = str(appointment.date)

			#time field
			if Appointment.objects.filter(date=date).count()>1:
				ap_last = Appointment.objects.filter(date=date).order_by('-id')[1]
				appointment.time=ap_last.time + datetime.timedelta(minutes=15)
			else:
				y,m,d = date.split('-')
				time = datetime.datetime(int(y),int(m),int(d),9,30)
				appointment.time = time

			all_appointment = Appointment.objects.filter(date=date).count()
			sn = "{:04}".format(all_appointment)
			appointment.serial=sn

			# appointment.time = time
			appointment.save()
			subject = 'Appointment serial for Mr.'+doctor.first_name+' '+doctor.last_name
			message = 'Thank You! '+str(request.user.first_name)+' '+str(request.user.last_name)+'. Here is your serial number on date '+str(appointment.time)+'. Your serial number is '+ str(sn)
			patient_email = str(appointment.email)
			send_mail(
				subject,
			    message,
			    'servicehospital07@gmail.com',
			    [patient_email],
			    fail_silently=False,
			    )
			return redirect('account:user_profile', username=request.user.username)

		context = {
			'form':form,
			'doctor':doctor,
		}
		return render(request, self.template_name,context)

#------- Lab -------#
class LabDetails(View):
	template_name = 'home/lab_details.html'

	def get(self, request):
		labs = Lab.objects.all()
		context = {
			'labs':labs,
		}
		return render(request, self.template_name, context)

#------- Pharmacy Medicine Details -------#
class CategoryMedicineDetails(View):
	template_name = 'home/category_medicine_details.html'
	def get(self, request,med_category):
		medicines = Pharmacy.objects.filter(medicine_category__slug=med_category)
		category = CategoryMedicine.objects.get(slug=med_category)
		contexts = {
			'category':category,
			'medicines':medicines,
		}
		return render(request, self.template_name, contexts)

#------- Pharmacy -------#
class PharmacyDetails(View):
	template_name = 'home/pharmacy.html'
	def get(self, request):
		medicines = Pharmacy.objects.all()[:4]
		medicine_category = CategoryMedicine.objects.all()

		contexts = {
			'medicine_category':medicine_category,
			'medicines':medicines,
		}
		return render(request, self.template_name, contexts)


#------- Medicine details -------#
class MedicineDetails(View):
	template_name = 'home/medicine_details.html'
	def get(self, request, slug):
		medicines = Pharmacy.objects.filter(medicine_category__slug=slug)
		cart_count = Cart.objects.filter(user=request.user).count()
		contexts = {
			'medicines':medicines,
			'cart_count':cart_count,
		}
		return render(request, self.template_name, contexts)

#------- Add to Cart medicine -------#
def update_cart(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
	if request.method == 'POST':
		product_id = request.POST['product_id']
		action = request.POST['action']
		print(action)

		customer = UserProfile.objects.get(id=request.user.id)
		product = Pharmacy.objects.get(id=product_id)

		cart , created = Cart.objects.get_or_create(user=customer, product=product)
		
		if action=='add':
			cart.save()
		elif action=='remove':
			cart.delete()
		elif action=='up' or action=='down':
			quantity = request.POST['quantity']
			per_price = request.POST['per_price']
			cart.count = quantity
			cart.per_price = per_price
			cart.save()

		total_carts = Cart.objects.filter(user=customer).count()
		total_price = sum([ c.per_price for c in Cart.objects.filter(user=customer)])
		print(total_carts)
		return JsonResponse({'status':'ok','total_carts':total_carts,'total_price':total_price})

#------- payment ------------#
def charge(request):
	if request.method == "POST":
		carts = Cart.objects.filter(
			user = request.user,
		)
		subtotal = round(sum(float(cart.per_price) for cart in carts), 2)
		total = subtotal

		#shipping address
		first_name = request.POST['firstname']
		last_name = request.POST['lastname']
		email = request.POST['email'] 
		country = request.POST['country'] 
		street_address = request.POST['address1'] 
		phone = request.POST['phone'] 


		shipping_address, created = ShippingAddress.objects.get_or_create(user = request.user)
		if created==True:
			shipping_address.first_name = first_name
			shipping_address.last_name = last_name
			shipping_address.email = email
			shipping_address.country = country
			shipping_address.street_address = street_address
			shipping_address.phone = phone

			shipping_address.save()

		if request.POST['transactionId'] !='':
			user = UserProfile.objects.get(email=request.user.email)
		else:
			user_name = request.POST['firstname'] + request.POST['lastname']
			customer = stripe.Customer.create(
				email = request.POST['email'],
				name = user_name,
				source = request.POST['stripeToken'],
			)
			charge = stripe.Charge.create(
				customer = customer,
				amount=500,
				currency = 'usd',
				description = 'Donation',
			)

		return redirect('account:user_profile',username=request.user.username)

def success(request, args):
	amount = args
	contexts = {
		'amount':amount,
	}
	return render(request, 'home/success.html', contexts)

#------- Cart Details -----------#
class CartDetails(View):
	template_name = 'home/cart_details.html'
	def get(self,request):
		cart_items = Cart.objects.filter(user__email=request.user.email)
		cart_count = len(cart_items)
		total_price = sum([ c.per_price for c in cart_items])

		contexts = {
			'cart_items':cart_items,
			'cart_count':cart_count,
			'total_price':total_price,
		}
		return render(request, self.template_name, contexts)

#------- Cart Details -----------#
class Checkout(View):
	template_name = 'home/checkout.html'
	def get(self, request):
		cart_items = Cart.objects.filter(user__email=request.user.email)		
		cart_price = round(sum([ c.per_price for c in cart_items]),2)
		shipping_price = 30.00
		total_price = cart_price + shipping_price
		contexts = {
			'cart_items':cart_items,
			'cart_price':cart_price,
			'shipping_price':shipping_price,
			'total_price': total_price,
		}
		return render(request, self.template_name, contexts)

#------- Food Blog -------#
class FoodBlogDetails(View):
	template_name = 'home/food_blog.html'
	def get(self, request):
		food_blogs = FoodBlog.objects.all().order_by('-id')
		contexts = {
			'food_blogs': food_blogs,
		}
		return render(request, self.template_name, contexts)

#------- food search list -------#
class FoodBlogSearch(ListView):
	model = FoodBlog
	template_name = 'home/food_search_results.html'
	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = FoodBlog.objects.filter(
			Q(title__icontains=query) | Q(description__icontains=query) | Q(date__icontains=query)
		)
		return object_list

#------- Food Blog -------#
class FoodBlogPost(View):
	template_name = 'home/flog_blog_post.html'
	def get(self, request, slug):
		food_blog_post = FoodBlog.objects.get(slug=slug)
		contexts = {
			'post':food_blog_post,
		}
		return render(request, self.template_name, contexts)

