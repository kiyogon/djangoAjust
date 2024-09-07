# ajust_pj/urls.py

from django.urls import path
from ajust_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<str:event_url>/', views.event_detail, name='event_detail'),
]