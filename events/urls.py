from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
	path('signup/', views.Signup.as_view(), name='signup'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),

	path('dashboard/', views.dashboard, name='dashboard'),

	path('events/', views.event_list, name='event-list'),
	path('events/<int:event_id>/', views.event_detail, name='event-detail'),

	path('create/event/', views.event_create, name='event-create'),
	path('event/<int:event_id>/update/', views.event_update, name='event-update'),
	path('event/<int:event_id>/deletd/', views.event_delete, name='event-delete'),
]
