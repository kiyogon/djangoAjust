# app/admin.py

from django.contrib import admin
from .models import Event, EventDate, Availability

class EventDateInline(admin.TabularInline):
    model = EventDate

class AvailabilityInline(admin.TabularInline):
    model = Availability

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventDateInline]

@admin.register(EventDate)
class EventDateAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline]
