from django.urls import path
from events import views
from events_api import views as apiviews
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
	path('', views.home, name='home'),
	path('signup/', views.Signup.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),

	path('dashboard/', views.dashboard, name='dashboard'),

	path('events/', views.event_list, name='event-list'),
	path('events/<int:event_id>/', views.event_detail, name='event-detail'),

	path('create/event/', views.event_create, name='event-create'),
	path('event/<int:event_id>/detail/', views.event_detail, name='event-detail'),
	path('event/<int:event_id>/book/', views.event_book, name='event-book'),
	path('event/<int:event_id>/update/', views.event_update, name='event-update'),
	path('event/<int:event_id>/deletd/', views.event_delete, name='event-delete'),



	#API URLS
	path('api/list/', apiviews.ListEvents.as_view(), name='event-list-api'),
	path('api/list/<int:organizer_id>/', apiviews.ListEventsOfOrganizer.as_view(), name='event-list-api'),
	path('api/list/booked-events/', apiviews.ListOfBookedEvents.as_view(), name='event-booked-list-api'),
	path('api/create/', apiviews.EventCreate.as_view(), name='event-create-api'),
	path('api/<int:event_id>/update', apiviews.EventUpdate.as_view(), name='event-update-api'),
	# path('api/<int:user_id>/', apiviews.EventAPIView.as_view(), name='event-detail-api'),


	path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/register/', apiviews.Register.as_view(), name='api-register'),

]
