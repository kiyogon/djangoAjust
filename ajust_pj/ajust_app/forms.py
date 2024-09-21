from django import forms
from .models import Event, DateOption, Participant, Response

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title']

class DateOptionForm(forms.ModelForm):
    class Meta:
        model = DateOption
        fields = ['date']
    
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['availability']
    
    availability = forms.ChoiceField(choices=Response.AVAILABILITY_CHOICES, widget=forms.RadioSelect)