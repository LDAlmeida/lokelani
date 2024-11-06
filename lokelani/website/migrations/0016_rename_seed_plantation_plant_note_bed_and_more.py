# Generated by Django 5.1 on 2024-11-06 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20241106_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantation',
            old_name='seed',
            new_name='plant',
        ),
        migrations.AddField(
            model_name='note',
            name='bed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.plantbeds'),
        ),
        migrations.AlterField(
            model_name='cyclicevent',
            name='beds',
            field=models.ManyToManyField(blank=True, help_text='Bed number, i.e: 1,2 ou 1-3', to='website.plantbeds'),
        ),
        migrations.AlterField(
            model_name='cyclicevent',
            name='frequency',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('biweekly', 'Every two weeks'), ('monthly', 'Monthly'), ('2.5months', 'Every 2 and a half months'), ('4months', 'Every 4 months')], max_length=50),
        ),
        migrations.AlterField(
            model_name='plant',
            name='name',
            field=models.CharField(help_text='Plant name, i.e: Rose, Gardenia', max_length=255),
        ),
        migrations.AlterField(
            model_name='plantbeds',
            name='name',
            field=models.CharField(blank=True, help_text='Bed number, i.e: 1,2 ou 1-3', max_length=255, null=True),
        ),
    ]
