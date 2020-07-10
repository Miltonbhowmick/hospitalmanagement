from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from multiselectfield import MultiSelectField
# Create your models here.
import os

def gen_code():
	uuid = os.urandom(1).hex()
	return uuid

class UserProfileManager(BaseUserManager):
	def create_user(self, email, phone=None, password=None, **kwargs):
		if not email:
			raise ValueError("User must have an email address!")
		email = self.normalize_email(email)
		user = self.model(email=email, phone=phone)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, email, password):
		user = self.create_user(email=email, password=password)
		user.is_superuser=True
		user.is_staff = True

		user.save(using=self._db)
		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):

	#basic info
	username = models.CharField(max_length=255, null=True, blank=True)
	first_name = models.CharField(max_length=255,null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=100, unique=True)
	phone = models.CharField(max_length=100,null=True, blank=True)

	#image
	user_image = models.ImageField(upload_to='user_images', null=True, blank=True)

	#about company structure
	division = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserProfileManager()

	USERNAME_FIELD = 'email'

	class Meta:
		ordering = ('-first_name',)

	def __str__(self):
		return self.email

	def save(self, *args, **kwargs):
		if not self.username:
			self.username = str(self.email.split('@')[0])+ str(gen_code())
		return super(UserProfile, self).save(*args, **kwargs)

#----- Staff Profile -----#
class Staff(models.Model):
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
		('Laboratory Director','Laboratory Director'),
		('Pathology Assistant','Pathology Assistant'),
	)
	DEGREE = (
		(1,'Bsc'),
		(2,'Diploma'),
	)
	username = models.CharField(max_length=255, null=True, blank=True)
	first_name = models.CharField(max_length=255,null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=100, unique=True)
	phone = models.CharField(max_length=100,null=True, blank=True)
	staff_image = models.ImageField(upload_to='doctor_images',null=True, blank=True)
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
		if not self.username:
			self.username = str(self.email.split('@')[0])+ str(gen_code())
		return super(Staff, self).save(*args, **kwargs)

