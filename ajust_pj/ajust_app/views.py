# ajust_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .models import Event, Date, Participant, Response
from .forms import EventForm, DateForm, ParticipantForm, ResponseForm

def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        DateFormSet = formset_factory(DateForm, extra=5, max_num=5)
        date_formset = DateFormSet(request.POST)
        
        if event_form.is_valid() and date_formset.is_valid():
            event = event_form.save()
            for date_form in date_formset:
                if date_form.cleaned_data:
                    date = date_form.save(commit=False)
                    date.event = event
                    date.save()
            return redirect('event_detail', event_id=event.id)
    else:
        event_form = EventForm()
        DateFormSet = formset_factory(DateForm, extra=5, max_num=5)
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
                availability = request.POST.get(f'date_{date.id}')
                if availability:
                    Response.objects.create(
                        participant=participant,
                        date=date,
                        availability=availability
                    )
            return redirect('event_detail', event_id=event.id)
    else:
        participant_form = ParticipantForm()
    
    responses = Response.objects.filter(date__event=event).select_related('participant', 'date')
    response_matrix = []
    for participant in participants:
        participant_responses = {date: '' for date in dates}
        for response in responses.filter(participant=participant):
            participant_responses[response.date] = response.get_availability_display()
        response_matrix.append({
            'participant': participant,
            'responses': [participant_responses[date] for date in dates]
        })
    
    context = {
        'event': event,
        'dates': dates,
        'participant_form': participant_form,
        'response_matrix': response_matrix,
    }
    return render(request, 'ajust_app/event_detail.html', context)