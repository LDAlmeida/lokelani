# lunar_calendar/management/commands/populate_moon_phases.py

import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from website.models import MoonPhase, MoonPhaseEvent

class Command(BaseCommand):
    help = 'Populate the database with moon phases'

    def handle(self, *args, **kwargs):
        base_url = 'https://api.farmsense.net/v1/moonphases/'
        start_date = timezone.now().date()
        
        for i in range(60):
            date = start_date + timedelta(days=i)
            date_time = datetime.combine(date, datetime.min.time())
            timestamp = int(date_time.timestamp())
            response = requests.get(base_url, params={'d': timestamp})
            if response.status_code == 200:
                data = response.json()
                print(f"Date: {date}, Timestamp: {timestamp}, Response: {data}")  # Imprime a resposta da API para verificação
                if data:
                    moon_data = data[0]
                    conventional_phase = moon_data.get('Phase', 'Unknown')
                    try:
                        MoonPhaseEvent.objects.update_or_create(
                            date= timezone.make_aware(datetime.fromtimestamp(timestamp)),
                            defaults={'moon_phase': MoonPhase.objects.get(phase=conventional_phase)}
                        )
                    except:
                        print("Invalid phase")
                    self.stdout.write(self.style.SUCCESS(f'Successfully added phase for {date}'))
                else:
                    self.stdout.write(self.style.ERROR(f'No data found for {date}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to retrieve data for {date}, status code: {response.status_code}'))
                