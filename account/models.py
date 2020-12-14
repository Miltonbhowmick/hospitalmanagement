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
	
	status = models.BooleanField (default = False)
	
	#image
	user_image = models.ImageField(upload_to='user_images', null=True, blank=True)

	#about company structure
	division = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	date = models.DateTimeField(auto_now_add=True, null=True)

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

