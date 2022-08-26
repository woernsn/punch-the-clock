from django.urls import path

from . import views

urlpatterns = [
    # Index goes to list
    path('', views.timelog_list, name='list'),

    # REST API
    path('api/punch', views.apiPunch, name='punch'),

    # Web UI
    path('token', views.token, name='token'),
    path('list', views.timelog_list, name='timelog_list', kwargs={'sorting': 'desc'}),
    path('calendar', views.timelog_calendar, name='timelog_calendar'),
    path('details/<int:timelog_id>', views.timelog_details, name='timelog_details')
]
