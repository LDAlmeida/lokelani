# Generated by Django 5.1 on 2024-09-02 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_moonphase'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoonPhaseEventPage',
            fields=[
                ('eventpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.eventpage')),
            ],
            options={
                'verbose_name': 'CodeRed Event',
                'abstract': False,
            },
            bases=('website.eventpage',),
        ),
    ]
