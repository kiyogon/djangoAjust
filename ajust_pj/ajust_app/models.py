# ajust_app/models.py

from django.db import models
import uuid

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Date(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()

    def __str__(self):
        return f"{self.event.name} - {self.date}"

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.event.name}"

class Response(models.Model):
    AVAILABILITY_CHOICES = [
        ('Y', '◯'),
        ('M', '△'),
        ('N', '✕'),
    ]
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='responses')
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES)

    class Meta:
        unique_together = ['participant', 'date']

    def __str__(self):
        return f"{self.participant.name} - {self.date.date} - {self.get_availability_display()}"
