# ajust_app/models.py
from django.db import models
import uuid

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Date(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)

class Response(models.Model):
    AVAILABILITY_CHOICES = [
        ('yes', '◯'),
        ('maybe', '△'),
        ('no', '✕'),
    ]
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='responses')
    availability = models.CharField(max_length=5, choices=AVAILABILITY_CHOICES)
