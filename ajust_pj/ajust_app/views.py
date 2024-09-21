# ajust_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .models import Event, Date, Participant, Response
from .forms import EventForm, DateFormSet, ParticipantForm, ResponseFormSet

def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        date_formset = DateFormSet(request.POST)
        if event_form.is_valid() and date_formset.is_valid():
            event = event_form.save()
            date_formset.instance = event
            date_formset.save()
            return redirect('event_detail', event_id=event.id)
    else:
        event_form = EventForm()
        date_formset = DateFormSet()
    return render(request, 'ajust_app/create_event.html', {
        'event_form': event_form,
        'date_formset': date_formset,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    dates = event.dates.all()
    participants = event.participants.all()

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        if participant_form.is_valid():
            participant = participant_form.save(commit=False)
            participant.event = event
            participant.save()
            for date in dates:
                Response.objects.create(participant=participant, date=date)
            return redirect('event_detail', event_id=event.id)
    else:
        participant_form = ParticipantForm()

    # 参加者ごとの回答状況を整理
    participant_responses = []
    for participant in participants:
        responses = {response.date: response.get_availability_display() for response in participant.responses.all()}
        participant_responses.append({
            'name': participant.name,
            'responses': [responses.get(date, '') for date in dates]
        })

    # 日付ごとの回答状況を集計
    date_summary = []
    for date in dates:
        yes_count = Response.objects.filter(date=date, availability='Y').count()
        maybe_count = Response.objects.filter(date=date, availability='M').count()
        no_count = Response.objects.filter(date=date, availability='N').count()
        date_summary.append({
            'date': date.date,
            'yes': yes_count,
            'maybe': maybe_count,
            'no': no_count
        })

    context = {
        'event': event,
        'dates': dates,
        'participant_form': participant_form,
        'participant_responses': participant_responses,
        'date_summary': date_summary,
    }
    return render(request, 'ajust_app/event_detail.html', context)

def participant_response(request, event_id, participant_id):
    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(Participant, id=participant_id, event=event)
    
    if request.method == 'POST':
        formset = ResponseFormSet(request.POST, instance=participant)
        if formset.is_valid():
            formset.save()
            return redirect('event_detail', event_id=event.id)
    else:
        formset = ResponseFormSet(instance=participant)
    
    return render(request, 'ajust_app/participant_response.html', {
        'event': event,
        'participant': participant,
        'formset': formset,
    })
