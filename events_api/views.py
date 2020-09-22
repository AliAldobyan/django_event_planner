from django.shortcuts import render

from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .serializers import EventSerializer, RegisterSerializer, EventBookingsSerializer, EventCreateUpdateSerializer
from events.models import Event, Booking
from .permissions import IsOrganizer


class Register(CreateAPIView):
	serializer_class = RegisterSerializer


class ListEvents(ListAPIView):
	serializer_class = 	EventSerializer

	def get_queryset(self):
		today = datetime.today()
		return Event.objects.filter(date__gt=today)


class ListEventsOfOrganizer(ListAPIView):
	serializer_class = 	EventSerializer

	def get_queryset(self):
			return Event.objects.filter(organizer=self.kwargs['organizer_id'])


class ListOfBookedEvents(ListAPIView):
	serializer_class = 	EventBookingsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
			return Booking.objects.filter(user = self.request.user)


class EventCreate(CreateAPIView):
	serializer_class = EventCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)


class EventUpdate(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateUpdateSerializer
	permission_classes = [IsOrganizer]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
