from django.db import models
from account import models as account_model
from django.utils.text import slugify
# Create your models here.

#----- Contact -----#
class Contact(models.Model):
	name = models.CharField(max_length=255, blank=True)
	email = models.CharField(max_length=255, blank=True)
	message = models.TextField(max_length=255, blank=True)
	reply = models.TextField(max_length=255, blank=True, default='')
	update = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)+'-'
		return super(Contact,self).save(*args, **kwargs)

