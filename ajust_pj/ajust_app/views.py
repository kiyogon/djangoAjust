from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Event, DateOption, Participant, Response
from .forms import EventForm, ParticipantForm

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            for date in form.cleaned_data['dates']:
                DateOption.objects.create(event=event, date=date)
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'ajust_app/create_event.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    date_options = event.date_options.all().order_by('date')
    participants = event.participants.all()

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
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
        form = ParticipantForm()

    participation_data = []
    for date_option in date_options:
        date_responses = {
            'date': date_option.date,
            'yes_count': Response.objects.filter(date_option=date_option, availability='Y').count(),
            'no_count': Response.objects.filter(date_option=date_option, availability='N').count(),
            'maybe_count': Response.objects.filter(date_option=date_option, availability='M').count(),
        }
        participation_data.append(date_responses)

    context = {
        'event': event,
        'date_options': date_options,
        'participants': participants,
        'form': form,
        'participation_data': participation_data,
    }
    return render(request, 'ajust_app/event_detail.html', context)