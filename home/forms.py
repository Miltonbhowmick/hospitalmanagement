from django import forms
from django.contrib.auth import authenticate
import re
from django.contrib.admin.widgets import AdminDateWidget
from .models import Appointment
# import from local
import os
import datetime

def gen_code():
	uuid = os.urandom(1).hex()
	return uuid

class AppointmentForm(forms.Form):
	first_name = forms.CharField(max_length=255, required=True,
		widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'First Name',
				}
			)
		)
	last_name = forms.CharField(max_length=255, required=True,
		widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Last Name',
				}
		)
	)
	email = forms.CharField(max_length=100, required=True,
		widget = forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'E-mail',
				}
		)
	)
	phone_number = forms.CharField(max_length=20, required=True,
			widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Phone Number',
				}
			)
		)
	age = forms.CharField(max_length=20, required=True,
			widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Your age',
				}
			)
		)
	address = forms.CharField(max_length=100, required=True,
			widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Address',
				}
			)
		)
	city = forms.CharField(max_length=50, required=True,
			widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'City',
				}
			)
		)
	division = forms.CharField(max_length=50, required=True,
			widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Division',
				}
			)
		)

	YEARS= ['2020',]
	MONTHS = {
		1:('July'),
	}
	date = forms.DateField(label='Select treatment date', widget=forms.SelectDateWidget(years=YEARS,months=MONTHS))

	def clean(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		phone_number = self.cleaned_data.get('phone_number')
		age = self.cleaned_data.get('age')
		address = self.cleaned_data.get('address')
		city = self.cleaned_data.get('city')
		division = self.cleaned_data.get('division')
		date = self.cleaned_data.get('date')

		if first_name.isalpha == False:
			raise forms.ValidationError('Please enter a real name!')
		else:
			if first_name[0].isupper()==False or first_name[1:].isupper()==True:
				raise forms.ValidationError('Please Capitalize properly!')
			else:
				if last_name.isalpha == False:
					raise forms.ValidationError('Please enter a real name!')
				else:
					if last_name[0].isupper()==False or last_name[1:].isupper()==True:
						raise forms.ValidationError('Please Capitalize properly!')						
					else:
						if len(email)<1:
							raise forms.ValidationError('Please enter email address!')
						else:
							email_correction = re.match('^[_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*(\.[a-zA-Z]{2,4})$',email)
							if not email_correction:
								raise forms.ValidationError('Please enter a valid email!')
							else:
								chk=phone_number[0]+phone_number[1]+phone_number[2]+phone_number[3]+phone_number[4]+phone_number[5]
										
								if chk!="+88017" and chk!="+88018" and chk!="+88019" and chk!="+88013" and chk!="+88016" and chk!="+88015":
									print("134124")
									raise forms.ValidationError('Invalid Phone number!')
								else:											
									if len(phone_number)!=11 and len(phone_number)!=14:
										raise forms.ValidationError('Invalid asdasdPhone number!')


	def deploy(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		phone_number = self.cleaned_data.get('phone_number')
		age = self.cleaned_data.get('age')
		address = self.cleaned_data.get('address')
		city = self.cleaned_data.get('city')
		division = self.cleaned_data.get('division')
		date = self.cleaned_data.get('date')
		appointment = Appointment(first_name=first_name,last_name=last_name,email=email,phone=phone_number,age=age,address=address,city=city,division=division,date=date)
		appointment.save()
		return appointment