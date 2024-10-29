from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.core.management.base import BaseCommand
from website.models import MoonPhaseEvent, MoonPhaseEventPage, EventIndexPage
from datetime import timedelta
import pytz

class Command(BaseCommand):
    help = 'Populate the database with moon phases'

    def handle(self, *args, **kwargs):
        eventos_pagina = EventIndexPage.objects.get(title="Plant Calendar")
        moon_phases = MoonPhaseEvent.objects.all().order_by('datetime')
        
        honolulu_tz = pytz.timezone('Pacific/Honolulu')
        start_datetime = None
        current_phase = None

        # Função auxiliar para criar e publicar eventos de fases lunares
        def create_and_publish_event(start, end, phase):
            existing_event = MoonPhaseEventPage.objects.filter(
                occurrences__start=start,
                occurrences__end=end,
            ).exists()
            
            if not existing_event:
                evento = MoonPhaseEventPage(
                    title=phase.phase,
                    calendar_color=phase.calendar_color,
                    first_published_at=timezone.now(),
                    last_published_at=timezone.now(),
                )
                eventos_pagina.add_child(instance=evento)
                evento.occurrences.create(start=start, end=end)
                evento.save_revision().publish()
                print(f"Evento criado para fase: {phase.phase}, de {start} a {end}")

        for i, phase_event in enumerate(moon_phases):
            if phase_event.moon_phase != current_phase:
                if current_phase is not None:
                    end_datetime = phase_event.datetime - timedelta(days=1)
                    end_datetime = make_aware(end_datetime.replace(hour=23, minute=59), honolulu_tz) if is_naive(end_datetime) else end_datetime.astimezone(honolulu_tz).replace(hour=23, minute=59)
                    start_datetime = make_aware(start_datetime, honolulu_tz) if is_naive(start_datetime) else start_datetime.astimezone(honolulu_tz)
                    
                    create_and_publish_event(start_datetime, end_datetime, current_phase)

                current_phase = phase_event.moon_phase
                start_datetime = make_aware(phase_event.datetime, honolulu_tz) if is_naive(phase_event.datetime) else phase_event.datetime.astimezone(honolulu_tz)

        # Finalize o último evento fora do loop
        if current_phase is not None:
            end_datetime = make_aware(moon_phases.last().datetime.replace(hour=23, minute=59), honolulu_tz) if is_naive(moon_phases.last().datetime) else moon_phases.last().datetime.astimezone(honolulu_tz).replace(hour=23, minute=59)
            create_and_publish_event(start_datetime, end_datetime, current_phase)