# ajust_pj/urls.py

from django.contrib import admin
from django.urls import path
from ajust_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.create_event, name='create_event'),
    path('event/<uuid:event_id>/', views.event_detail, name='event_detail'),
    path('event/<uuid:event_id>/participant/<int:participant_id>/', views.participant_response, name='participant_response'),
]
