from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	organizer = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	time = models.TimeField()
	date = models.DateField()
	location = models.TextField(blank=True)
	capacity = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.title


class Booking(models.Model):
	event = models.ForeignKey(Event , on_delete = models.CASCADE, related_name='bookings')
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	tickets = models.IntegerField()

	def get_total_tickets(self):
		bookings = self.bookings
		number_of_tickets = 0
		for book in  bookings:
			number_of_tickets += book.tickets

		return number_of_tickets


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)
