from django.db import models
from account.models import UserProfile
from home.models import Pharmacy
from .utils import generate_order_id
from .choices import *

# Create your models here.

#------ Shipping Address -------#
class ShippingAddress(models.Model):
	user = models.ForeignKey(
		UserProfile,
		on_delete = models.CASCADE,
		null=True,
		blank=True,
		related_name = 'shipping_addresses',
	)
	session_id = models.CharField(max_length=100,null=True, blank=True)
	email = models.CharField(max_length=50, null=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	phone = models.CharField(max_length=50)
	street_address = models.CharField(max_length=255)

	is_default = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username if self.user else self.session_id

#----- Cart ------#
class Cart(models.Model):
	user = models.ForeignKey(
		UserProfile, 
		on_delete=models.CASCADE, 
		blank=True,
		related_name ='carts',
	)
	product = models.ForeignKey(
		Pharmacy, 
		blank=True, 
		on_delete=models.CASCADE,
		related_name='products',
	)
	count = models.IntegerField(default=1)
	per_price = models.FloatField()
	is_active = models.BooleanField(default=True)

	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.email + ' : ' + self.product.name

	def save(self, *args, **kwargs):
		self.per_price = round((self.product.price * float(self.count)), 3)
		return super(Cart, self).save(*args, **kwargs)
	class Meta:
		ordering = ('-date',)

#------- Payment --------#
class Payment(models.Model):
	order = models.ForeignKey(
		'Order',
		on_delete = models.CASCADE,
		related_name = 'payments',
	)

	status = models.CharField(
		max_length=100,
		choices = PaymentStatusChoice.choices,
		default = PaymentStatusChoice.PENDING
	)

	chash_on_delivery = models.BooleanField(default=False)
	card = models.BooleanField(default=False)
	mobile_banking = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100)

	amount = models.FloatField(default=0)
	shipping_price = models.FloatField(default=0)

	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.order.order_id + ' : ' + self.status

#------- Order Status -------#
class OrderStatus(models.Model):
	order = models.ForeignKey(
		'Order',
		on_delete=models.CASCADE,
		related_name = 'statuses',
	)
	on_type = models.CharField(
		max_length = 100,
		choices = StatusChoice.choices,
		default = StatusChoice.PENDING_PAYMENT,
	)

	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.order.order_id + ' : ' + self.on_type

#------- Order --------#
class Order(models.Model):
	order_id = models.CharField(max_length=20)
	user = models.ForeignKey(
		UserProfile,	
		on_delete = models.CASCADE,
		null=True,
		blank=True,
		related_name='orders',
	)
	session_id = models.CharField(max_length=100, null=True, blank=True)
    
	carts = models.ManyToManyField(Cart)
	
	shipping_address = models.ForeignKey(
		ShippingAddress,
		on_delete = models.SET_NULL,
		null=True,
		blank=True,
		related_name = 'shipping_addresses',
	)
	order_note = models.TextField(max_length=500, null=True, blank=True)
	status = models.ForeignKey(
		OrderStatus,
		on_delete = models.SET_NULL,
		null=True,
		blank=True,
		related_name='statuses'
	)
	payment = models.ForeignKey(
		Payment,
		on_delete = models.SET_NULL,
		null=True,
		blank=True,
		related_name = 'payments',
	)
	date = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if not self.order_id:
			self.order_id = generate_order_id()
		super().save()

	def __str__(self):
		return self.order_id + ' : ' + self.status.on_type

