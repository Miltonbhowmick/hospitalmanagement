from django.shortcuts import render, redirect
from django.views import View
from .forms import AddProductForm, AddBlogForm, EditProductForm, EditUserDetailsForm, EditOrderForm,ContactBoxForm

from . import models as staff_model
from home import models as store_model
from account import models as account_model
from sell import models as sell_model

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db.models import Q
import datetime

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
		sold = sell_model.Order.objects.filter(status='delivered').count()
		available = products.filter(is_publish=True).count()
		unpublish = total_product-available
		new_products = products.order_by('-id')[:4]

		# order details
		orders = sell_model.Order.objects.all()
		total_order = orders.count() - orders.filter(status='refunded').all().count()
		pending_order = orders.filter(status = 'pending_payment').all().count()
		processing_order = orders.filter(status = 'processing').all().count()
		in_transit_order = orders.filter(status = 'in_transit').all().count()
		delivered_order = orders.filter(status = 'delivered').all().count()
		new_orders = orders.order_by('-id')[:4]
		
		contexts = {
			'total_users':total_users,
			'online_users':online_users,
			'offline_users': offline_users,
			'new_users':new_users,

			'total_blog':total_blog,
			'popular_blogs':popular_blogs,

			'total_product':total_product,
			'sold':sold,
			'available':available,
			'unpublish':unpublish,
			'new_products':new_products,

			'total_order':total_order,
			'pending_order':pending_order,
			'processing_order':processing_order,
			'in_transit_order': in_transit_order,
			'delivered_order': delivered_order,
			'new_orders':new_orders,
		}
		return render(request, self.template_name, contexts)

# ------ User Profile --------#
class UserDetailes(View):
	template_name = 'staff/user/user.html'

	def get(self, request, username):
		user = account_model.UserProfile.objects.get(username = username)
		form = EditUserDetailsForm(instance = user)
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)
	def post(self, request, username):
		user = account_model.UserProfile.objects.get(username = username)
		form = EditUserDetailsForm(request.POST or None, instance = user)
		if form.is_valid():
			is_active = form.cleaned_data.get('is_active')
			if is_active:
				user.is_active=True
			else:
				user.is_active=False
			user.save()
			return redirect('staff:user_list')
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ User List --------#
class UserList(View):
	template_name = 'staff/user/user_list.html'

	def get(self, request):
		
		search_by = request.GET.get('search')
		order_by = request.GET.get('order_by','-date')

		if search_by:
			users = account_model.UserProfile.objects.filter(Q(is_staff=False) & (Q(username__icontains=search_by)| Q(email__icontains=search_by) | Q(phone__icontains=search_by)) ).order_by(order_by.lower()).all()
		else:
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
			form.save()
			return redirect('staff:product')
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ Order List -----------#
class OrderList(View):
	template_name = 'staff/order/order_list.html'

	def get(self, request):

		direction_by = request.GET.get('dir_by','desc')
		search_by = request.GET.get('search')
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
		if search_by:
			orders = sell_model.Order.objects.filter( Q(order_id__icontains=search_by) | Q(user__email__icontains=search_by) | Q(payment__status__icontains=search_by) ).order_by(order_by.lower()).all()
		else:
			orders = sell_model.Order.objects.order_by(order_by.lower()).all()

		# order pagination
		paginator = Paginator(orders, 6)
		page = request.GET.get('page')
		try:
			all_orders = paginator.get_page(page)
		except PageNotAnInteger:
			all_orders = paginator.get_page(page)
		except EmptyPage:
			all_orders = paginator.get_page(page)

		contexts = {
			'all_orders': all_orders,
			'order_by': order_by,
			'direction_by': direction_by,
			'direction_column': direction_column,
		}
		return render(request, self.template_name, contexts)

# ------ Edit Order -----------#
class EditOrder(View):
	template_name = 'staff/order/edit_order.html'

	def get(self, request, id):
		order = sell_model.Order.objects.get(id=id)
		form = EditOrderForm(instance=order)
		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)
	def post(self, request, id):
		order = sell_model.Order.objects.get(id=id)

		payment_status ,created = sell_model.Payment.objects.get_or_create(order=order)

		form = EditOrderForm(request.POST or None, instance=order)

		if form.is_valid():
			order.status = form.cleaned_data.get('status')
			order.save()
			payment_status.status = form.cleaned_data.get('payment')
			payment_status.save()
			order.payment = payment_status

			order.save()

			return redirect('staff:order_list')

		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ Blog -----------#
class Blog(View):
	template_name = 'staff/blog/blog.html'

	def get(self, request):

		# post view 
		see = request.GET.get('view')
		if see:
			return redirect('home:food_blog_post', slug=see)

		# sort column by values
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
		form = AddBlogForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			form.deploy()
			return redirect('staff:blog')

		contexts = {
			'form':form,
		}
		return render(request, self.template_name, contexts)

# ------ Contact Box --------- #
class ContactBox(View):
	template_name = 'staff/contact/contact_box.html'
	def get(self, request):
		contacts = staff_model.Contact.objects.filter(update__date = datetime.date.today())
		contexts = {
			'contacts':contacts,
		}
		return render(request, self.template_name, contexts)
	def post(self, request):
		date = request.POST['select_date']
		sel_date = datetime.datetime.strptime(date,'%Y-%m-%d').date()

		contacts = staff_model.Contact.objects.filter(update__date = sel_date)
		contexts = {
			'contacts':contacts,
		}
		return render(request, self.template_name, contexts)

class ContactBoxDetails(View):
	template_name = 'staff/contact/contact_details.html'
	def get(self, request,id):
		contact = staff_model.Contact.objects.get(id=id)
		form = ContactBoxForm(instance=contact)
		
		contexts = {
			'form':form,
			'contact':contact,
		}
		return render(request, self.template_name, contexts)
	def post(self, request, id):
		contact = staff_model.Contact.objects.get(id=id)
		form = ContactBoxForm(request.POST or None, instance=contact)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			subject = "YourCare Hospital- Solution"
			message = form.cleaned_data.get('message')
			reply = form.cleaned_data.get('message')
			content = message + reply
			send_mail(
	            subject,
	            content,
	            "servicehospital07@gmail.com",
	            [email],
			    fail_silently=False,
	        )
		contexts = {
			'form':form,
			'contact':contact,
		}
		return render(request, self.template_name, contexts)

# ------ product delete ------- #
def product_delete(request, slug):
	store_model.Pharmacy.objects.get(slug=slug).delete()
	return redirect('staff:product')

# ------ blog delete -------- #
def blog_delete(request, id):
	store_model.FoodBlog.objects.get(id=id).delete()
	return redirect('staff:blog')




