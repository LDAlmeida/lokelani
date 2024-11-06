from django.shortcuts import render
from website.models import PlantBeds, CyclicEvent, EventPage
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

def plant_bed(request, bed_id):
    bed = PlantBeds.objects.get(id=bed_id)
    cyclic_events = CyclicEvent.objects.filter(beds=bed)
    return render(request, 'website/plant_bed_page.html', {'plant_bed': bed, 'cyclic_events': cyclic_events})

def delete_event(request, event_id):
    event = get_object_or_404(EventPage, id=event_id)
    if request.method == "POST":
        event.delete()
        return redirect("/plant-calendar")
