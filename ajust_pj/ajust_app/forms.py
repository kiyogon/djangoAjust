# ajust_app/forms.py

from django import forms
from .models import Event, EventDate, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']

class EventDateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'availability']