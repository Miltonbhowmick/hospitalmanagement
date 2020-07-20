from django import forms
from django.contrib.auth import authenticate
import re

# import from local
from .models import UserProfile

import os

def gen_code():
	uuid = os.urandom(1).hex()
	return uuid

class LoginForm(forms.Form):
	email = forms.CharField(max_length=255,required=False,
		widget=forms.TextInput(
				attrs ={
					'class': 'form-control',
					'placeholder': 'youremail@gmail.com',
				}
			)
		)
	password = forms.CharField(max_length=255, required=False,
		widget = forms.PasswordInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'password',
				}
			)
		)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if len(email)<1:
			raise forms.ValidationError('Enter your email address!')
		else:
			email_correction = re.match('^[_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z]+(\.[a-zA-Z0-9]+)*(\.[a-zA-Z]{2,4})$',email)
			if not email_correction:
				raise forms.ValidationError('Email is not correct!')
			else:
				if len(password)<1:
					raise forms.ValidationError('Enter your password!')
				else:
					user = authenticate(email=email,password=password)
					if not user:
						raise forms.ValidationError('Invalid email and password. Please try again!')
					else:
						if not user.is_active:
							raise forms.ValidationError('Something with your ID. Please contact with customer service!')

	def login_request(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		user = authenticate(email=email, password=password)

		return user	


class UserRegistrationForm(forms.Form):
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
	password1 = forms.CharField(max_length=255, required=True,
		widget = forms.PasswordInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Password',
				}
		)
	)
	password2 = forms.CharField(max_length=255, required=True,
		widget = forms.PasswordInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Confirm-Password',
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

	def clean(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		phone_number = self.cleaned_data.get('phone_number')

		if first_name.isalpha == False:
			raise forms.ValidationError('Please enter a real name!')
		else:
			if first_name[0].isupper()==False or first_name[1:].isupper()==True:
				raise forms.ValidationError('Please First Name Capitalize properly!')
			else:
				if last_name.isalpha == False:
					raise forms.ValidationError('Please enter a real name!')
				else:
					if last_name[0].isupper()==False or last_name[1:].isupper()==True:
						raise forms.ValidationError('Please Last Name Capitalize properly!')						
					else:
						if len(email)<1:
							raise forms.ValidationError('Please enter email address!')
						else:
							email_correction = re.match('^[_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*(\.[a-zA-Z]{2,4})$',email)
							if not email_correction:
								raise forms.ValidationError('Please enter a valid email!')
							else:
								if UserProfile.objects.filter(email=email).exists():
									raise forms.ValidationError("User is already exist!, please choose new one")
								else:
									if len(password1)<8:
										raise forms.ValidationError('Password is too short!')
									else:
										if password1!=password2:
											raise forms.ValidationError('Password is not matched!')
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
		phone = self.cleaned_data.get('phone')
		password1 = self.cleaned_data.get('password1')
		phone_number = self.cleaned_data.get('phone_number')

		user_name = str(email.split('@')[0])+ str(gen_code())

		user = UserProfile(username=user_name, first_name=first_name, last_name=last_name, email=email, phone=phone_number)
		user.set_password(password1)
		user.is_active = False
		user.save()
		return user

