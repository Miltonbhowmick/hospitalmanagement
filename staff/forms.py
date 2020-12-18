from django import forms
from account import models as account_model
from home import models as store_model 
from sell import models as sell_model
from sell.choices import StatusChoice, PaymentStatusChoice
from ckeditor.fields import RichTextFormField

# ------- add product -------- #
class EditUserDetailsForm(forms.ModelForm):
	class Meta:
		model = account_model.UserProfile
		fields = ('first_name','last_name','username','email','phone', 'address','city','division','is_active')

		widgets = {
			'first_name': forms.TextInput(
				attrs = {
					'class':'form-control',
					'readonly':'readonly',
				}
			),	
			'last_name': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'username': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'email': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'phone': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'address': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'city': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'division': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'readonly':'readonly',
				}
			),
			'is_active':forms.CheckboxInput(
				attrs = {
					'class':'form-check-input',
					'type':'checkbox',
				}
			)
		}		

# ------- add product -------- #
class AddProductForm(forms.Form):
	name = forms.CharField(
		max_length=255,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Product name', 
				'type':'text',
			}
		)
	)
	image = forms.ImageField(
		widget = forms.ClearableFileInput(
			attrs = {
			}
		)
	)
	description = RichTextFormField()

	category = forms.ModelChoiceField(
		queryset=store_model.CategoryMedicine.objects.all(),
		required=True,
		empty_label="--Category--",
		widget = forms.Select(
			attrs = {
				'class': 'form-control',

			}
		)
	)

	price = forms.FloatField(
		initial=0.0, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter current price!',
				'type':'number',
				'step':'0.001',
			}
		)
	)
	quantity = forms.IntegerField( 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Quantity',
				'type':'number',
				'step':'1',
			}
		)
	)

	def clean(self):
		name = self.cleaned_data.get('name')
		description = self.cleaned_data.get('description')
		image = self.cleaned_data.get('image')
		price = self.cleaned_data.get('price')
		category = self.cleaned_data.get('category')
		quantity = self.cleaned_data.get('quantity')

		if not name:
			raise forms.ValidationError("Enter product name!")
		if not price:
			raise forms.ValidationError("Enter price!")
		if not quantity:
			raise forms.ValidationError("Enter quantity")

	def deploy(self):
		name = self.cleaned_data.get('name')
		description = self.cleaned_data.get('description')
		image = self.cleaned_data.get('image')
		price = self.cleaned_data.get('price')
		category = self.cleaned_data.get('category')
		quantity = self.cleaned_data.get('quantity')

		product, created = store_model.Pharmacy.objects.get_or_create(
			name = name,
			description = description,
			price = price,
			medicine_category = category,
			quantity = quantity,
		)
		product.medicine_image = image
		product.save()
		
		return product




# ------- Edit Product Form ------- #
class EditProductForm(forms.ModelForm):
	class Meta:
		model = store_model.Pharmacy
		fields = ('name','medicine_image','medicine_category','company','quantity','price')
		widgets = {
			'name': forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder': 'Product name', 
					'type':'text',
				}
			),
			'medicine_image': forms.ClearableFileInput(
				attrs = {
							
				}
			),
			'medicine_category' : forms.Select(
				attrs = {
					'class':'form-control',
				}
			),
			'company' : forms.Select(
				attrs = {
					'class':'form-control',
				}
			),
			'quantity' : forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder': 'Enter current price!',
				}
			),
			'price' : forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Enter current price!',
					'type':'number',
				}
			),
		}

	def deploy(self):
		name = self.cleaned_data.get('name')
		price = self.cleaned_data.get('price')
		category = self.cleaned_data.get('medicine_category')
		company = self.cleaned_data.get('company')
		quantity = self.cleaned_data.get('quantity')
		image = self.cleaned_data.get('medicine_image')

		product, created = store_model.Pharmacy.objects.get_or_create(
			name = name,
			price = price,
			medicine_category = category,
			quantity = quantity,
		)
		product.medicine_image = image
		return product

# ------- Edit Order Form ------- #  
class EditOrderForm(forms.ModelForm):

	payment = forms.ChoiceField(
		choices = PaymentStatusChoice.choices,
		widget = forms.Select(
			attrs = {
				'class':'form-control',
			}
		)
	)

	class Meta:
		model = sell_model.Order
		fields = ('order_id','user','carts','shipping_address', 'status')

		widgets = {
			'order_id': forms.TextInput(
				attrs = {
					'class':'form-control',
					'readonly':'readonly',
				}
			),
			'user': forms.Select(
				attrs = {
					'class':'form-control',
					'readonly':'readonly',
				}
			),
			'carts': forms.SelectMultiple(
				attrs = {
					'class':'form-control',
					'readonly':'readonly',
				}
			),
			'shipping_address': forms.Select(
				attrs = {
					'class':'form-control',
					'readonly':'readonly',
				}
			),
			'status': forms.Select(
				attrs = {
					'class':'form-control',
				}
			),
		}

# ------- Add Blog Form ------- #  
class AddBlogForm(forms.Form):
	title = forms.CharField(
		max_length=100,
		widget = forms.TextInput(
			attrs = {
				'class': 'form-control',
				'placeholder': 'Enter blog title',
			}
		)
	)

	image = forms.ImageField(
		required=False,
		widget = forms.ClearableFileInput(
			attrs = {
				'style':'display:block;',
			}		
		)
	)

	description = RichTextFormField()

	def clean(self):
		title = self.cleaned_data.get('title')
		image = self.cleaned_data.get('image')
		description = self.cleaned_data.get('description')

	def deploy(self):
		title = self.cleaned_data.get('title')
		image = self.cleaned_data.get('image')
		description = self.cleaned_data.get('description')

		blog, created = store_model.FoodBlog.objects.get_or_create(
			title = title,
			description = description
		)
		blog.post_image = image
		blog.save()

		return blog


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
