# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<uuid:slug>/', views.event_detail, name='event_detail'),
    path('event/create/', views.create_event, name='create_event'),
]
