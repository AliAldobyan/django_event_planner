from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
	path('signup/', views.Signup.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),

	path('dashboard/', views.Dashboard, name='dashboard'),
	path('events/', views.EventList, name='event-list'),
	path('create/event/', views.EventCreate, name='event-create'),
	path('event/<int:event_id>/update/', views.EventUpdate, name='event-update'),
	path('event/<int:event_id>/deletd/', views.EventDelete, name='event-delete'),
]
