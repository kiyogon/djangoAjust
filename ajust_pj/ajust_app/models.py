# ajust_app/models.py

from django.db import models
import uuid

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()

    class Meta:
        unique_together = ['event', 'date']

    def __str__(self):
        return f"{self.event.name} - {self.date}"

class Participant(models.Model):
    AVAILABILITY_CHOICES = [
        ('O', '◯'),
        ('X', '✕'),
        ('D', '△'),
    ]
    name = models.CharField(max_length=100)
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE, related_name='participants')
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES)

    class Meta:
        unique_together = ['name', 'event_date']

    def __str__(self):
        return f"{self.name} - {self.event_date} - {self.get_availability_display()}"
