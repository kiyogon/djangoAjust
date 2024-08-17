# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventDate, Availability
from .forms import EventForm, EventDateForm, AvailabilityForm
from django.forms import modelformset_factory


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    # 出欠状況の計算
    availability_results = {}
    max_available_count = 0
    participants = set()

    for event_date in event.dates.all():
        availabilities = event_date.availabilities.all()
        available_count = availabilities.filter(choice='O').count()
        unavailable_count = availabilities.filter(choice='X').count()
        maybe_count = availabilities.filter(choice='D').count()

        max_available_count = max(max_available_count, available_count)

        # 参加者リストを更新
        for availability in availabilities:
            participants.add(availability.name)

        availability_results[event_date] = {
            'availabilities': availabilities,
            'available_count': available_count,
            'unavailable_count': unavailable_count,
            'maybe_count': maybe_count,
        }

    participants = sorted(participants)  # 名前順に並び替え

    return render(request, 'event_detail.html', {
        'event': event,
        'availability_results': availability_results,
        'max_available_count': max_available_count,
        'participants': participants,
    })


def create_event(request):
    EventDateFormSet = modelformset_factory(EventDate, form=EventDateForm, extra=10)  # 最大10個の日時を選択可能
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        formset = EventDateFormSet(request.POST, queryset=EventDate.objects.none())
        if event_form.is_valid() and formset.is_valid():
            event = event_form.save()
            for form in formset:
                if form.cleaned_data.get('date'):
                    event_date = form.save(commit=False)
                    event_date.event = event
                    event_date.save()
            return redirect('event_detail', slug=event.slug)
    else:
        event_form = EventForm()
        formset = EventDateFormSet(queryset=EventDate.objects.none())
    return render(request, 'create_event.html', {'event_form': event_form, 'formset': formset})