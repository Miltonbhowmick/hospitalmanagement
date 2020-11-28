from django import forms


#------- Contact Form -------#
class ContactForm(forms.Form):

	name = forms.CharField(max_length=255, required=True,
		widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Your Name....',
				}
			)
		)
	email = forms.CharField(max_length=255, required=True,
		widget = forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Your Mail....',
				}
			)
		)
	message = forms.CharField(widget=forms.Textarea)

	def clean(self):
		name = self.cleaned_data.get('name')
		email = self.cleaned_data.get('email')
		message = self.cleaned_data.get('message')
		if name.isalpha == False:
			raise forms.ValidationError('Please enter a real name!')
		else:
			if name[0].isupper()==False or name[1:].isupper()==True:
				raise forms.ValidationError('Please Capitalize properly!')
			else:
				if len(email)<1:
					raise forms.ValidationError('Please enter email address!')
				else:
					email_correction = re.match('^[_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*(\.[a-zA-Z]{2,4})$',email)
					if not email_correction:
						raise forms.ValidationError('Please enter a valid email!')

	def deploy(self):
		name = self.cleaned_data.get('name')
		email = self.cleaned_data.get('email')
		message = self.cleaned_data.get('message')

		contact = Contact(name=name,email=email, message=message)
		contact.save()
