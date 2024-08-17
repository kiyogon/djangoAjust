# app/models.py

from django.db import models
import uuid

class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='dates', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.event.name} - {self.date}"

class Availability(models.Model):
    event_date = models.ForeignKey(EventDate, related_name='availabilities', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    choice = models.CharField(max_length=2, choices=[('O', '◯'), ('X', '✕'), ('D', '△')])

    def __str__(self):
        return f"{self.name}: {self.choice} ({self.event_date.date})"

