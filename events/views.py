from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from datetime import datetime

from .models import Event, Booking
from .forms import UserSignup, UserLogin, EventForm

def home(request):
	return render(request, 'home.html')


def Dashboard(request):
	event_by_date = Event.objects.filter(date__gt = datetime.today())
	events = Event.objects.filter(organizer = request.user)
	bookings = Booking.objects.filter(user = request.user)
	if request.user.is_anonymous:
		redirect('login')
	past_events = []
	for books in bookings:
		if books.event.date < datetime.today().date():
			past_events.append(books
			)
	context = {
	"events" : events,
	"past_events": past_events,
	}

	return render(request,"dashboard.html",context)


def EventList(request):
	events = Event.objects.filter(date__gt = datetime.today())

	query = request.GET.get("q")
	if query:
		events = events.filter(
		Q(title__icontains=query)|
		Q(description__icontains=query)|
		Q(organizer__username__icontains=query)|
		Q(date__icontains=query)
		).distinct()

	bookings = Booking.objects.filter(event=events)

	context = {
	"events" : events,
	"bookings":bookings,
	}
	return render(request,'event_list.html',context)


def EventCreate(request):
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


def EventUpdate(request,event_id):
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


def EventDelete(request,event_id):
	event = Event.objects.get(id = event_id)
	if request.user != event.organizer:
		return redirect('login')
	event.delete()
	messages.warning(request,"You have successfully Deleted An Event.")
	return redirect('dashboard')


# def EventDetail(request, event_id):



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
				messages.success(request, "Welcome Back!")
				return redirect('home')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")
