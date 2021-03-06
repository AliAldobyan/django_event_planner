from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking

class UserSignup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets={
		'password': forms.PasswordInput(),
		}


class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['organizer']

		widgets = {
			'time': forms.TimeInput(attrs={'type':'time'}),
			'date': forms.DateInput(attrs={'type':'date'}),
		}


class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		exclude = ['user','event']


class ProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = "__all__"
