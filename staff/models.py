from django.db import models
from account import models as account_model

from channels.db import database_sync_to_async
# Create your models here.

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

