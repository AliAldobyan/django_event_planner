from events.models import Event , Booking
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

		fields = ['first_name','last_name']

class EventSerializer(serializers.ModelSerializer):
	organizer = UserSerializer
	class Meta:
		model = Event
		fields = ['title', 'date','organizer']


class EventDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class EventBookingsSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ['user', 'event', 'tickets']

	def get_event(self, obj):
		return obj.event.title

class EventCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['organizer']



class EventBookerSerializer(serializers.ModelSerializer):
	pass




class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username','password','first_name','last_name']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		new_user = User(username=username, first_name=first_name, last_name=last_name)
		new_user.set_password(password)
		new_user.save()
		return validated_data
