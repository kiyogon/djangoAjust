# ajust_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.db import transaction
from .models import Event, EventDate, Participant
from .forms import EventForm, EventDateForm, ParticipantForm
import random
import string
import logging

logger = logging.getLogger(__name__)

def generate_unique_url():
    while True:
        url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        if not Event.objects.filter(url=url).exists():
            return url

@transaction.atomic
def index(request):
    EventDateFormSet = formset_factory(EventDateForm, extra=5, max_num=5)
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        date_formset = EventDateFormSet(request.POST)
        if event_form.is_valid() and date_formset.is_valid():
            try:
                event = event_form.save(commit=False)
                event.url = generate_unique_url()
                event.save()
                for form in date_formset:
                    if form.cleaned_data.get('date'):
                        EventDate.objects.create(event=event, date=form.cleaned_data['date'])
                return redirect('event_detail', event_url=event.url)
            except Exception as e:
                logger.error(f"Error creating event: {str(e)}")
                return render(request, 'ajust_app/index.html', {
                    'event_form': event_form,
                    'date_formset': date_formset,
                    'error': 'イベントの作成中にエラーが発生しました。もう一度お試しください。'
                })
    else:
        event_form = EventForm()
        date_formset = EventDateFormSet()
    return render(request, 'ajust_app/index.html', {
        'event_form': event_form,
        'date_formset': date_formset
    })

def event_detail(request, event_url):
    event = get_object_or_404(Event, url=event_url)
    event_dates = event.dates.all().order_by('date')
    
    if request.method == 'POST':
        forms = []
        for event_date in event_dates:
            form_data = {
                'name': request.POST.get('name'),
                'availability': request.POST.get(f'availability_{event_date.id}')
            }
            form = ParticipantForm(form_data)
            if form.is_valid():
                participant = form.save(commit=False)
                participant.event_date = event_date
                try:
                    participant.save()
                except Exception as e:
                    logger.error(f"Error saving participant: {str(e)}")
                    return render(request, 'ajust_app/event_detail.html', {
                        'event': event,
                        'event_dates': event_dates,
                        'error': '参加情報の保存中にエラーが発生しました。もう一度お試しください。'
                    })
            else:
                forms.append(form)
        if not forms:
            return redirect('event_detail', event_url=event_url)
    
    participants = Participant.objects.filter(event_date__event=event).order_by('name', 'event_date__date')
    participation_data = {}
    for participant in participants:
        if participant.name not in participation_data:
            participation_data[participant.name] = {}
        participation_data[participant.name][participant.event_date.date] = participant.get_availability_display()
    
    # データを整形
    formatted_data = [
        {
            'name': name,
            'availabilities': [dates.get(date.date, '-') for date in event_dates]
        }
        for name, dates in participation_data.items()
    ]
    
    return render(request, 'ajust_app/event_detail.html', {
        'event': event,
        'event_dates': event_dates,
        'formatted_data': formatted_data
    })
