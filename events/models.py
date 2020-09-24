from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Event(models.Model):
	organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'events')
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	time = models.TimeField()
	date = models.DateField()
	location = models.TextField(blank=True)
	capacity = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.title


	def get_total_tickets(self):
		bookings = self.bookings.all()

		number_of_tickets = sum([booking.tickets for booking in bookings])

		return  self.capacity - number_of_tickets


class Booking(models.Model):
	event = models.ForeignKey(Event , on_delete = models.CASCADE, related_name='bookings')
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	tickets = models.IntegerField()

	def __str__(self):
		return f"{self.event.title} - {self.user.username}"


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()
