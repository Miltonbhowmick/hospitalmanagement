from django.db import models
from django.utils.text import slugify 
from multiselectfield import MultiSelectField
# Create your models here.
import os
import datetime

def gen_code():
	uuid = os.urandom(1).hex()
	return uuid

#### DOCTOR CATEGORY ####
class Category(models.Model):
	name = models.CharField(max_length=255,null=True, blank=True)
	slug = models.SlugField(unique=True, blank=True, default='')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Category,self).save(*args, **kwargs)		

#### DOCTOR PROFILE ####
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
	doctor_category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

class Appointment(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True,blank=True)
	first_name = models.CharField(max_length=255,null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=100)
	phone = models.CharField(max_length=100,null=True, blank=True)
	age = models.CharField(max_length=100,null=True, blank=True)
	#address
	address = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	division = models.CharField(max_length=255, null=True, blank=True)
	#date
	date = models.DateField(default=datetime.date.today)
	#serial
	serial = models.CharField(max_length=100,null=True, blank=True)

	def __str__(self):
		return self.email
