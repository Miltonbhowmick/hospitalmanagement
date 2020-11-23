from django.db import models
from django.utils.text import slugify 
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from account.models import UserProfile
import os
import datetime

#----- Generate random -----#
def gen_code():
	uuid = os.urandom(1).hex()
	return uuid

#----- Category -----#
class Category(models.Model):
	name = models.CharField(max_length=255,null=True, blank=True)
	slug = models.SlugField(unique=True, blank=True, default='')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Category,self).save(*args, **kwargs)		

#----- Doctor Profile -----#
class Doctor(models.Model):
	GENDER = (
		('male','Male'),
		('female','Female'),
	)
	RELIGION = (
		('islam','Islam'),
		('Hindu','Hindu'),
		('buddhist','Buddhist'),
		('cristian ','Cristian'),
	)
	DESIGNATION = (
		('medical-officer','Medical Officer'),
		('assistant-professor','Assistant Professor'),
		('associate-professor','Associate Professor'),
		('Professor ','Professor'),
	)
	DEGREE = (
		(1,'MBBS'),
		(2,'MBBCh'),
		(3,'PhD'),
		(4,'MPhil'),
		(5,'FRCS'),
		(6,'DTCD'),
		(7,'FCCP'),
		(8,'D-Card'),

	)
	doctor_category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
	first_name = models.CharField(max_length=255,null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=100, unique=True)
	phone = models.CharField(max_length=100,null=True, blank=True)
	doctor_image = models.ImageField(upload_to='doctor_images',null=True, blank=True)
	designation = models.CharField(max_length=255,choices= DESIGNATION, null=True, blank=True)
	degree = MultiSelectField(max_length=255,max_choices=5, choices=DEGREE, null=True, blank=True)
	gender = models.CharField(max_length=25,choices = GENDER, null=True, blank=True)
	religion = models.CharField(max_length=255, choices=RELIGION, null=True, blank=True)
	#address
	division = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)

	slug = models.SlugField(unique=True, blank=True, default='')

	def __str__(self):
		return self.email

	def save(self, *args, **kwargs):
		self.slug = slugify(self.first_name)+'-'+slugify(self.last_name)+'-'
		return super(Doctor,self).save(*args, **kwargs)


#----- Appointment model -----#
class Appointment(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL,null=True,blank=True)
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,null=True,blank=True)
	first_name = models.CharField(max_length=255,null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=100)
	phone = models.CharField(max_length=100,null=True, blank=True)
	age = models.CharField(max_length=100,null=True, blank=True)
	urgent_resolve = models.BooleanField(default=False)
	#address
	address = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	division = models.CharField(max_length=255, null=True, blank=True)
	#date and time
	date = models.DateField(default=datetime.date.today)
	time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	#serial
	serial = models.CharField(max_length=100,null=True, blank=True)
	complete = models.BooleanField(default=False)

	def __str__(self):
		return self.email

#----- Lab model -----#
class Lab(models.Model):
	name = models.CharField(max_length=255,blank=True, default='')
	cost = models.IntegerField(null=True, blank=True)
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Lab,self).save(*args, **kwargs)		

#----- Pharmacy model -----#
class MedicineCompany(models.Model):
	name = models.CharField(max_length=255, blank=True, default='')
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(MedicineCompany,self).save(*args, **kwargs)


#----- Pharmacy model -----#
class CategoryMedicine(models.Model):
	name = models.CharField(max_length=255, blank=True, default='')
	image = models.ImageField(max_length=255, blank=True)	
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(CategoryMedicine,self).save(*args, **kwargs)		

#----- Pharmacy model -----#
class Pharmacy(models.Model):
	name = models.CharField(max_length=255, blank=True, default='')
	medicine_image = models.ImageField(upload_to='medcine_images', null=True, blank=True)
	formatted_image = ImageSpecField(source='medicine_image', processors=[ResizeToFill(100,100)], format='JPEG',options={'quantity':60})
	company = models.ForeignKey(MedicineCompany, on_delete=models.SET_NULL, null=True, blank=True)
	medicine_category = models.ForeignKey(CategoryMedicine, on_delete=models.SET_NULL, null=True, blank=True) 
	quantity = models.IntegerField(blank=True, default=1)
	price = models.FloatField(blank=True, default=1.00)
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Pharmacy,self).save(*args, **kwargs)		

#----- Medicine Cart ------#
class Cart(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True)
	products = models.ForeignKey(Pharmacy, blank=True, on_delete=models.CASCADE)
	count = models.IntegerField(default=1)
	per_price = models.FloatField()

	date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		return self.user.email

	def save(self, *args, **kwargs):
		self.per_price = round((self.products.price * float(self.count)), 3)
		return super(Cart, self).save(*args, **kwargs)
	class Meta:
		ordering = ('-date',)

#----- Food blog model -----#
class FoodBlog(models.Model):
	title = models.CharField(max_length=255, blank=True, default='')
	date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
	post_image = models.ImageField(upload_to='medcine_images', null=True, blank=True)
	thumbnail = ImageSpecField(source='post_image', processors=[ResizeToFill(100,200)], format='JPEG', options={'quality':60})
	description = RichTextField(max_length=1000, null=True, blank=True)
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)+'-'
		return super(FoodBlog,self).save(*args, **kwargs)		

#----- Contact -----#
class Contact(models.Model):
	name = models.CharField(max_length=255, blank=True, default='')
	email = models.CharField(max_length=255, blank=True, default='')
	message = models.TextField(max_length=255, blank=True, default='')

	def __str__(self):
		return self.email
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Contact,self).save(*args, **kwargs)		

