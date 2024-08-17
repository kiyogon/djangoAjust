# app/forms.py

from django import forms
from .models import Event, EventDate, Availability

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']

class EventDateForm(forms.ModelForm):
    class Meta:
        model = EventDate
        fields = ['date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'})  # カレンダーから日付を選択できるようにする
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['choice']  # 'name' フィールドを除外し、'choice' のみを使用
        widgets = {
            'choice': forms.RadioSelect(choices=[
                ('O', '◯'),
                ('X', '✕'),
                ('D', '△'),
            ])
        }
