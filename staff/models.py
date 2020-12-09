from django.db import models
from account import models as account_model

from channels.db import database_sync_to_async
# Create your models here.


class ConnectionHistory(models.Model):
	ONLINE = 'online'
	OFFLINE = 'offline'
	STATUS = (
	    (ONLINE, 'On-line'),
	    (OFFLINE, 'Off-line'),
	)
	user = models.ForeignKey(
		account_model.UserProfile,
	    on_delete=models.CASCADE
	)	
	device_id = models.CharField(max_length=100)
	status = models.CharField(max_length=10, choices=STATUS,default=ONLINE)
	first_login = models.DateTimeField(auto_now_add=True)
	last_echo = models.DateTimeField(auto_now=True)

	class Meta:
	    unique_together = (("user", "device_id"),)

	def __str__(self):
		return self.user

	# ------ online/offline ------ #

	@database_sync_to_async
	def update_user_status(self, user, device_id, status):
		return staff_model.ConnectionHistory.objects.get_or_create(
		    user=user, device_id=device_id,
		).update(status=status)


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

