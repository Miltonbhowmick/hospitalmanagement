from django import forms
from home import models as store_model 

from ckeditor.fields import RichTextFormField

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
