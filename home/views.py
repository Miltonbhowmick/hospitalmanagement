from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from .models import Doctor,Category,Appointment,Lab, MedicineCompany, Pharmacy, CategoryMedicine, FoodBlog
from .forms import AppointmentForm
from django.core.mail import send_mail
from django.db.models import Q

#------- Home -------#
class HomeInfo(View):
	template_name = 'home/home.html'
	def get(self, request):
		doctors = Doctor.objects.all()
		categories = Category.objects.all()
		appointments = Appointment.objects.all()
		urgent_resolve = Appointment.objects.filter(Q(urgent_resolve=True) & Q(complete=True)).count()

		context = {
			'appointments':appointments,
			'doctors':doctors,
			'categories': categories,	
			'urgent_resolve':urgent_resolve,		
		}

		return render(request,self.template_name,context)

#------- Doctors of Category  -------#
class CategoryDoctor(View):
	template_name = 'home/doctor_details.html'

	def get(self, request, category):
		doctors = Doctor.objects.filter(doctor_category__slug=category)
		category = Category.objects.get(slug=category)
		context = {
			'category':category,
			'doctors':doctors,
		}
		if doctors:
			return render(request, self.template_name,context)
		else:
			return HttpResponse('No doctors')

#------- Doctor Info -------#
class DoctorInfo(View):
	template_name = 'home/doctor_info_details.html'

	def get(self, request,category, doctor):
		doctor = Doctor.objects.get(slug=doctor)
		context = {
			'doctor':doctor,
		}
		return render(request, self.template_name,context)

#------- Appointment -------#
class DoctorAppointment(View):
	template_name = 'home/appointment.html'
	def get(self, request,doctor):
		doctor = Doctor.objects.get(slug=doctor)
		form = AppointmentForm()
		context = {
			'form':form,
			'doctor':doctor,
		}
		return render(request, self.template_name,context)

	def post(self, request, doctor):
		doctor = Doctor.objects.get(slug=doctor)
		form = AppointmentForm(request.POST or None)
		if form.is_valid():
			appointment = form.deploy()
			appointment.doctor=doctor
			if request.user.is_authenticated:
				appointment.user = request.user
			appointment.save()
			

			date = str(appointment.date)
			all_appointment = Appointment.objects.filter(date=date).count()
			sn = "{:04}".format(all_appointment)
			appointment.serial=sn
			appointment.save()
			subject = 'Appointment serial for Mr.'+doctor.first_name+' '+doctor.last_name
			message = 'Here is your serial number on date '+date+'. Your serial number is '+ sn
			patient_email = str(appointment.email)
			send_mail(
				subject,
			    message,
			    'miltonbhowmick7@gmail.com',
			    [patient_email],
			    fail_silently=False,
			    )

		return HttpResponse()

#------- Lab -------#
class LabDetails(View):
	template_name = 'home/lab_details.html'

	def get(self, request):
		labs = Lab.objects.all()
		context = {
			'labs':labs,
		}
		return render(request, self.template_name, context)

#------- Pharmacy -------#
class PharmacyDetails(View):
	template_name = 'home/pharmacy.html'
	def get(self, request):
		medicines = Pharmacy.objects.all()[:4]
		medicine_category = CategoryMedicine.objects.all()

		contexts = {
			'medicine_category':medicine_category,
			'medicines':medicines,
		}
		return render(request, self.template_name, contexts)

#------- Pharmacy Medicine Details -------#
class CategoryMedicineDetails(View):
	template_name = 'home/category_medicine_details.html'
	def get(self, request,med_category):
		medicines = Pharmacy.objects.filter(medicine_category__slug=med_category)
		category = CategoryMedicine.objects.get(slug=med_category)
		contexts = {
			'category':category,
			'medicines':medicines,
		}
		return render(request, self.template_name, contexts)

#------- Food Blog -------#
class FoodBlogDetails(View):
	template_name = 'home/food_blog.html'
	def get(self, request):
		food_blogs = FoodBlog.objects.all().order_by('-id')
		print(food_blogs)
		contexts = {
			'food_blogs': food_blogs,
		}
		return render(request, self.template_name, contexts)

