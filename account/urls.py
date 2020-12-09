from django.urls import path
from django.conf.urls import url
from . import views
app_name = "account"

urlpatterns = [
	path('login/',views.Login.as_view(), name='login'),
	path('logout/',views.logout_request, name='logout'),
	path('sign-up/',views.SignUp.as_view(), name='signup'),
	path('<str:username>/',views.UserProfileView.as_view(), name='user_profile'),
	path('activate/<str:uidb64>/<str:token>/',views.activate_account, name='activate'),

]