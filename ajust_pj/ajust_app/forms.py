# ajust_app/forms.py
from django import forms
from .models import Event, Date, Participant, Response

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']

class DateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Date
        fields = ['date']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['availability']
