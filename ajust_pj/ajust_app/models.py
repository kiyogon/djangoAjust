from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class DateOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='date_options')
    date = models.DateField()

    def __str__(self):
        return f"{self.event.title} - {self.date}"

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Response(models.Model):
    AVAILABILITY_CHOICES = [
        ('Y', '○'),
        ('N', '✕'),
        ('M', '△'),
    ]
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    date_option = models.ForeignKey(DateOption, on_delete=models.CASCADE, related_name='responses')
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES)

    class Meta:
        unique_together = ['participant', 'date_option']

    def __str__(self):
        return f"{self.participant.name} - {self.date_option.date} - {self.get_availability_display()}"