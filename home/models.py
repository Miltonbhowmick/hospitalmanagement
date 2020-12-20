from django.db import models
from django.utils.text import slugify 
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .utils import _get_unique_slug
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

#----- Medicine Company model -----#
class MedicineCompany(models.Model):
	name = models.CharField(max_length=255, blank=True, default='')
	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(MedicineCompany,self).save(*args, **kwargs)


#----- Category Medicine model -----#
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
	name = models.CharField(max_length=255, default='')
	description = RichTextField()
	medicine_image = models.ImageField(upload_to='medcine_images')
	formatted_image = ImageSpecField(source='medicine_image', processors=[ResizeToFill(100,100)], format='JPEG',options={'quantity':60})
	company = models.ForeignKey(MedicineCompany, on_delete=models.SET_NULL, null=True, blank=True)
	medicine_category = models.ForeignKey(CategoryMedicine, on_delete=models.SET_NULL, null=True) 
	quantity = models.IntegerField(blank=True, default=1)
	price = models.FloatField(blank=True, default=1.00)

	is_publish = models.BooleanField(default=False)

	date = models.DateTimeField(auto_now_add=True,null=True)

	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = _get_unique_slug(self.name, self.__class__)
		return super(Pharmacy,self).save(*args, **kwargs)		

#----- Food blog model -----#

class FoodBlog(models.Model):
	title = models.CharField(max_length=255, blank=True, default='')
	date = models.DateTimeField(auto_now_add=True, blank=True)
	post_image = models.ImageField(upload_to='blog_images', null=True, blank=True)
	formatted_image = ImageSpecField(source='post_image', processors=[ResizeToFill(800,300)], format='JPEG', options={'quality':90})
	description = RichTextField(max_length=1000, null=True, blank=True)
	view = models.IntegerField(blank=True, default=0)

	slug = models.SlugField(unique=True,blank=True, default='')

	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)+'-'
		return super(FoodBlog,self).save(*args, **kwargs)		
	
#----- Food blog model -----#
class FoodBlogView(models.Model):
	foodblog = models.ForeignKey(
		'FoodBlog',
		on_delete = models.CASCADE,
		related_name='foodblog'
	)
	ip = models.GenericIPAddressField()
	session = models.CharField(blank=True, max_length=40)
	created = models.DateTimeField(default = datetime.datetime.now())

	def __str__(self):
		return self.foodblog.title


