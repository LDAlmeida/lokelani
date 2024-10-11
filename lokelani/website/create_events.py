from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from website.models import MoonPhaseEvent, MoonPhaseEventPage, EventIndexPage
from datetime import timedelta
import pytz

def create_moon_events():
    # Obter a página de eventos (Calendário)
    eventos_pagina = EventIndexPage.objects.get(title="Plant Calendar")
    
    # Obter todas as fases da lua do banco de dados ordenadas por data
    moon_phases = MoonPhaseEvent.objects.all().order_by('datetime')

    # Variáveis para armazenar o início e fim de cada fase
    start_datetime = None
    current_phase = None

    # Defina o fuso horário de Honolulu
    honolulu_tz = pytz.timezone('Pacific/Honolulu')

    for i, phase_event in enumerate(moon_phases):
        # Verificar se a fase atual mudou em relação à fase anterior, ou se é a primeira iteração
        if phase_event.moon_phase != current_phase:
            # Se não for a primeira iteração, crie o evento para a fase anterior
            if current_phase is not None:
                # Criar uma nova página de evento para a fase anterior
                evento = MoonPhaseEventPage(
                    title=current_phase.phase,
                    calendar_color=current_phase.calendar_color,
                    first_published_at=timezone.now(),
                    last_published_at=timezone.now(),
                )

                # Adicionar o evento como filho da página de eventos
                eventos_pagina.add_child(instance=evento)

                # Criar a data de término como o dia anterior à nova fase
                end_datetime = phase_event.datetime - timedelta(days=1)

                # Certifique-se de que a data de término seja "aware" e ajuste para o fuso horário de Honolulu
                if is_naive(end_datetime):
                    end_datetime = make_aware(end_datetime, honolulu_tz)
                else:
                    end_datetime = end_datetime.astimezone(honolulu_tz)

                # Ajuste a data de término para 23:59
                end_datetime = end_datetime.replace(hour=23, minute=59)
                #print(f"Start datetime: {start_datetime}, End datetime: {end_datetime}")

                # Ajustar start_datetime para o fuso horário de Honolulu
                if is_naive(start_datetime):
                    start_datetime = make_aware(start_datetime, honolulu_tz)
                else:
                    start_datetime = start_datetime.astimezone(honolulu_tz)

                # Criar a ocorrência para o evento
                evento.occurrences.create(
                    start=start_datetime,
                    end=end_datetime,
                )
                print(f"Start datetime: {start_datetime}, End datetime: {end_datetime}")

                # Publicar a página do evento
                evento.save_revision().publish()

            # Atualizar a fase atual e a data/hora de início
            current_phase = phase_event.moon_phase
            start_datetime = phase_event.datetime

            # Garantir que a data de início seja "aware" e ajustar para o fuso horário de Honolulu
            if is_naive(start_datetime):
                start_datetime = make_aware(start_datetime, honolulu_tz)
            else:
                start_datetime = start_datetime.astimezone(honolulu_tz)

    # Após o loop, criar o evento para a última fase
    if current_phase is not None:
        evento = MoonPhaseEventPage(
            title=current_phase.phase,
            calendar_color=current_phase.calendar_color,
            first_published_at=timezone.now(),
            last_published_at=timezone.now(),
        )

        eventos_pagina.add_child(instance=evento)

        # Ajustar a data de término da última fase
        if is_naive(phase_event.datetime):
            end_datetime = make_aware(phase_event.datetime.replace(hour=23, minute=59), honolulu_tz)
        else:
            end_datetime = phase_event.datetime.astimezone(honolulu_tz).replace(hour=23, minute=59)

        # Criar a última ocorrência
        evento.occurrences.create(
            start=start_datetime,
            end=end_datetime,
        )

        # Publicar a página do evento
        evento.save_revision().publish()
        
if __name__ == "__main__":
    create_moon_events()
