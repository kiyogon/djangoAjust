# ajust_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_event, name='create_event'),
    path('event/<uuid:event_id>/', views.event_detail, name='event_detail'),
]