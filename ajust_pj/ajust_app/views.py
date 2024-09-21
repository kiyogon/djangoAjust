from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .models import Event, DateOption, Participant, Response
from .forms import EventForm, DateOptionForm, ParticipantForm, ResponseForm

def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        DateOptionFormSet = formset_factory(DateOptionForm, extra=5, max_num=5)
        date_formset = DateOptionFormSet(request.POST)
        
        if event_form.is_valid() and date_formset.is_valid():
            event = event_form.save()
            for form in date_formset:
                if form.cleaned_data.get('date'):
                    DateOption.objects.create(event=event, date=form.cleaned_data['date'])
            return redirect('event_detail', event_id=event.id)
    else:
        event_form = EventForm()
        DateOptionFormSet = formset_factory(DateOptionForm, extra=5, max_num=5)
        date_formset = DateOptionFormSet()
    
    return render(request, 'ajust_app/create_event.html', {
        'event_form': event_form,
        'date_formset': date_formset,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    date_options = event.date_options.all()
    participants = event.participants.all()
    
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        if participant_form.is_valid():
            participant = participant_form.save(commit=False)
            participant.event = event
            participant.save()
            
            for date_option in date_options:
                availability = request.POST.get(f'availability_{date_option.id}')
                if availability:
                    Response.objects.create(
                        participant=participant,
                        date_option=date_option,
                        availability=availability
                    )
            return redirect('event_detail', event_id=event.id)
    else:
        participant_form = ParticipantForm()
    
    # Prepare data for the template
    date_option_data = []
    for date_option in date_options:
        responses = date_option.responses.all()
        yes_count = responses.filter(availability='Y').count()
        no_count = responses.filter(availability='N').count()
        maybe_count = responses.filter(availability='M').count()
        date_option_data.append({
            'date': date_option.date,
            'yes_count': yes_count,
            'no_count': no_count,
            'maybe_count': maybe_count,
        })
    
    return render(request, 'ajust_app/event_detail.html', {
        'event': event,
        'date_option_data': date_option_data,
        'participants': participants,
        'participant_form': participant_form,
    })