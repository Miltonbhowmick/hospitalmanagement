from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout 
# Create your views here.
from .forms import LoginForm, UserRegistrationForm
from .models import UserProfile
from home.models import Appointment

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# 404 page for wrong url
from django.http import Http404

def page_not_found(request,param):
	print(param)
	if not param:
		raise HttpResponseNotFound('<h1>No Page Here</h1>')
	return render_to_response('account/page_404.html')

class Login(View):
	template_name = 'account/login.html'
	def get(self,request):
		form = LoginForm()
		contexts = {
			'form': form,
		}
		return render(request, self.template_name,contexts)
	def post(self, request):

		form = LoginForm(request.POST or None)
		print(131312)
		if form.is_valid():
			user = form.login_request()
			if user:
				login(request, user)
				return redirect('home:home_info')
		contexts = {
			'form': form,
		}
		return render(request, self.template_name,contexts)

def logout_request(request):
	print(134141)
	logout(request)
	return redirect('home:home_info')

class SignUp(View):
	template_name = 'account/signup.html'

	def get(self, request):

		form = UserRegistrationForm()
		variables = {
			'form': form,
			}
		return render(request, self.template_name, variables)

	def post(self, request):
		form = UserRegistrationForm(request.POST or None)	

		if form.is_valid():
			user = form.deploy()
			current_site = get_current_site(request)
			email_subject = 'Activate Your Account'
			message = render_to_string('account/activate_account.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
				})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(email_subject, message, to=[to_email])
			email.send()
			return HttpResponse('We have sent you an email, please confirm your email address to complete registration')

		variables = {
		'form': form,
		}

		return render(request, self.template_name, variables)

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home:home_info')
    else:
        return HttpResponse('Activation link is invalid!')


class UserProfileView(View):
	template_name = 'account/user_profiles.html'
	def get(self, request, username):
		user_details = UserProfile.objects.get(username=username)
		appointments = Appointment.objects.filter(user__username=username).order_by('-id')
		contexts = {
			'appointments':appointments,
			'user_details': user_details,
		}		
		return render(request, self.template_name,contexts)
