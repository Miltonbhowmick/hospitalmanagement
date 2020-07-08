from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from .models import Doctor,Category,Appointment,Lab
from .forms import AppointmentForm
from django.core.mail import send_mail

#------- Home -------#
class HomeInfo(View):
	template_name = 'home/home.html'
	def get(self, request):
		doctors = Doctor.objects.all()
		categories = Category.objects.all()
		appointments = Appointment.objects.all()

		context = {
			'appointments':appointments,
			'doctors':doctors,
			'categories': categories,			
		}

		return render(request,self.template_name,context)

#------- Doctors of Category  -------#
class CategoryDoctor(View):
	template_name = 'home/doctor_details.html'

	def get(self, request, category):
		doctors = Doctor.objects.filter(doctor_category__slug=category)
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


