from django import forms



# ------- add product -------- #
class AddProduct(forms.Form):
	name = forms.CharField(max_length=255, required=False, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Product name', 
				'class': 'form-control'
			}
		)
	)
	price = forms.FloatField(required=False, initial=0.0, 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Enter current price!',
			}
		)
	)

	def clean(self):
		name = self.cleaned_data.get('name')
		price = self.cleaned_data.get('price')

		if not name:
			raise forms.ValidationError("Enter product name!")
		if not price:
			raise forms.ValidationError("Enter price!")

	def deploy(self, category):
		name = self.cleaned_data.get('name')
		price = self.cleaned_data.get('price')

		product = store_model.Product.objects.create(
			name=name,
			price=price
		)
		return product

# ------- Contact Form ------- #
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
