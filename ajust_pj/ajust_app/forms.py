from django import forms
from .models import Event, Participant
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):
    dates = forms.DateField(
        widget=forms.SelectDateWidget,
        required=True
    )
    date_options = forms.DateField(
        widget=forms.SelectDateWidget,
        required=False
    )

    class Meta:
        model = Event
        fields = ['title']

    def clean(self):
        cleaned_data = super().clean()
        dates = [cleaned_data.get('dates')] + [cleaned_data.get('date_options') for _ in range(4) if cleaned_data.get('date_options')]
        dates = list(filter(None, dates))
        if len(dates) > 5:
            raise ValidationError("最大5つまでの日付を選択できます。")
        cleaned_data['dates'] = dates
        return cleaned_data

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']