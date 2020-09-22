from rest_framework.permissions import BasePermission
from events.models import Event
class IsOrganizer(BasePermission):
	message = "you must be the event organizer!"

	def has_permission(self, request, view):
		event  = Event.objects.get(id=view.kwargs['event_id'])
		return event.organizer == request.user

	def has_object_permession(self,request,view,obj):
		if request.user == obj.organizer:
			return True
		return False
