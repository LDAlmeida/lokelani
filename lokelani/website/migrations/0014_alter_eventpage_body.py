# Generated by Django 5.1 on 2024-11-04 16:41

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_delete_plantbedpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', 0)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {})}, null=True),
        ),
    ]
