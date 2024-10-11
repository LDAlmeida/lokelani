# Generated by Django 5.1 on 2024-09-24 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_moonphaseevent_date_moonphaseevent_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclicevent',
            name='beds',
        ),
        migrations.AlterField(
            model_name='cyclicevent',
            name='calendar_color',
            field=models.CharField(blank=True, default='#123456', max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='cyclicevent',
            name='beds',
            field=models.ManyToManyField(blank=True, help_text='Número dos canteiros, ex: 1,2 ou 1-3', to='website.plantbeds'),
        ),
    ]