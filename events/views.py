from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from datetime import datetime
from django.db.models import Q

from .models import Event, Booking
from .forms import UserSignup, UserLogin, EventForm, BookingForm

def home(request):
	return render(request, 'home.html')


def dashboard(request):
	past_bookings = Booking.objects.filter(user = request.user, event__date__lt=datetime.today())
	if request.user.is_anonymous:
		redirect('login')

	context = {
	"past_bookings": past_bookings,
	}

	return render(request,"dashboard.html",context)


def event_list(request):
	events = Event.objects.filter(date__gt = datetime.today())

	query = request.GET.get("q")
	if query:
		events = events.filter(
		Q(title__icontains=query)|
		Q(description__icontains=query)|
		Q(organizer__username__icontains=query)|
		Q(date__icontains=query)|
		Q(location__icontains=query)
		).distinct()

	context = {
	"events" : events,
	}
	return render(request,'event_list.html',context)


def event_detail(request , event_id):
	event = Event.objects.get(id = event_id)

	context = {
	"event" : event,
	}
	return render(request,'event_detail.html',context)


def event_create(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			event_obj = form.save(commit=False)
			event_obj.organizer = request.user
			event_obj.save()
			messages.success(request, "You Have Successfully Created An Event.")
			return redirect('home')
	context = {
		"form":form,
	}
	return render(request, 'event_create.html', context)


def event_book(request,event_id):
	form = BookingForm()
	event = Event.objects.get(id=event_id)

	try:
		user_booking = Booking.objects.get(event=event, user=request.user)
	except Booking.DoesNotExist:
		user_booking = None

	if request.user.is_anonymous:
		return redirect('login')

	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			booking = form.save(commit = False)

			if booking.tickets > event.get_total_tickets():
				messages.warning(request,"Sorry , No seats enough to book!")

			else:
				booking.user = request.user
				booking.event= event
				booking.save()
				messages.success(request , "You Have Successfully Booked An Event.")
				return redirect("event-list")

	context = {
	"event" : event,
	"form" :form,
	"user_booking" : user_booking,
	}
	return render(request,'event_book.html',context)


def event_update(request,event_id):
	event_obj = Event.objects.get(id=event_id)
	if request.user != event_obj.organizer:
		return redirect('login')
	form = EventForm(instance = event_obj)
	if request.method == "POST":
		form = EventForm(request.POST, instance=event_obj)
		if form.is_valid():
			form.save()
			messages.success(request , "You have successfully Updated The Event.")
			return redirect('dashboard')
	context = {
		"form":form,
		"event": event_obj
	}
	return render(request, 'event_update.html', context)

def event_delete(request,event_id):
	event = Event.objects.get(id = event_id)
	if request.user != event.organizer:
		return redirect('login')
	event.delete()
	messages.warning(request,"You have successfully Deleted An Event.")
	return redirect('dashboard')


class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				if Event.objects.filter(organizer=auth_user).exists():
					return redirect('dashboard')
				messages.success(request, "Welcome Back!")
				return redirect('event-list')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")
