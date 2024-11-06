from typing import Iterable
from coderedcms.blocks import HTML_STREAMBLOCKS
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from coderedcms.blocks import BaseBlock
from coderedcms.blocks import BaseLinkBlock
from coderedcms.blocks import LinkStructValue
from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from coderedcms.models import CoderedPage
from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamBlock, RichTextBlock
from wagtail.fields import StreamField, RichTextField
from wagtail.snippets.models import register_snippet
from datetime import datetime, timedelta
import csv
from website.forms import EventCompletionForm

class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    body = StreamField(
        StreamBlock([
            ("rich_text", RichTextBlock()),
        ]),
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


# -- Navbar & Footer ----------------------------------------------------------

class NavbarLinkBlock(BaseLinkBlock):
    """
    Simple link in the navbar.
    """

    class Meta:
        icon = "link"
        label = "Link"
        template = "website/blocks/navbar_link.html"
        value_class = LinkStructValue

class NavbarDropdownBlock(BaseBlock):
    """
    Custom dropdown menu with heading, links, and rich content.
    """

    class Meta:
        icon = "arrow-down"
        label = "Dropdown"
        template = "website/blocks/navbar_dropdown.html"

    title = blocks.CharBlock(
        max_length=255,
        required=True,
        label="Title",
    )
    links = blocks.StreamBlock(
        [("link", NavbarLinkBlock())],
        required=True,
        label="Links",
    )
    description = blocks.StreamBlock(
        HTML_STREAMBLOCKS,
        required=False,
        label="Description",
    )

@register_snippet
class Navbar(models.Model):
    """
    Custom navigation bar / menu.
    """

    class Meta:
        verbose_name = "Navigation Bar"

    name = models.CharField(
        max_length=255,
    )
    content = StreamField(
        [
            ("link", NavbarLinkBlock()),
            ("dropdown", NavbarDropdownBlock()),
        ],
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("content"),
    ]

    def __str__(self) -> str:
        return self.name

@register_snippet
class Footer(models.Model):
    """
    Custom footer for bottom of pages on the site.
    """

    class Meta:
        verbose_name = "Footer"

    name = models.CharField(
        max_length=255,
    )
    content = StreamField(
        LAYOUT_STREAMBLOCKS,
        verbose_name="Content",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("content"),
    ]

    def __str__(self) -> str:
        return self.name

class MoonPhase(models.Model):
    phase = models.CharField(max_length=20)
    phase_hawaii = models.CharField(max_length=20)
    calendar_color = models.CharField(max_length=7, default="#000000")
    
    def __str__(self):
        return f"{self.phase} ({self.phase_hawaii})"
    
class MoonPhaseEvent(models.Model):
    datetime = models.DateTimeField(unique=True)
    moon_phase = models.ForeignKey(MoonPhase, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.datetime}: {self.moon_phase.phase}  ({self.moon_phase.phase_hawaii})"

class MoonPhaseEventPage(EventPage):
    pass

class MoonPhaseLoader:
    @classmethod
    def load_from_csv(cls, csv_file_path):
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lunation = int(row['Lunation'])

                # Carregar as fases da lua e associá-las com os eventos
                new_moon_phase = MoonPhase.objects.get(phase='New Moon')
                first_quarter_phase = MoonPhase.objects.get(phase='First Quarter')
                full_moon_phase = MoonPhase.objects.get(phase='Full Moon')
                third_quarter_phase = MoonPhase.objects.get(phase='Third Quarter')

                # Processar as fases da lua para cada linha do CSV
                cls.create_or_update_event(new_moon_phase, row['New Moon'])
                cls.create_or_update_event(first_quarter_phase, row['First Quarter'])
                cls.create_or_update_event(full_moon_phase, row['Full Moon'])
                cls.create_or_update_event(third_quarter_phase, row['Third Quarter'])

    @staticmethod
    def create_or_update_event(moon_phase, datetime_str):
        if datetime_str:  # Garantir que o valor não está vazio
            event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            MoonPhaseEvent.objects.update_or_create(
                datetime=timezone.make_aware(event_datetime),
                defaults={'moon_phase': moon_phase}
            )

class Seed(models.Model):
    name = models.CharField(max_length=255, help_text="Nome da semente, ex: Rosa, Gardênia")
    
    def __str__(self):
        return self.name

class Plantation(models.Model):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, related_name='plantations')
    plant_bed = models.ForeignKey('PlantBeds', on_delete=models.CASCADE, related_name='plantations')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.seed.name} x{self.quantity}"

class PlantBeds(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True, help_text="Número dos canteiros, ex: 1,2 ou 1-3")
    bed_number = models.IntegerField()
    
    def __str__(self):
        return self.name    
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Plant bed number {self.bed_number}"
        return super(PlantBeds, self).save(*args, **kwargs)

class CyclicEvent(models.Model):
    EVENT_FREQUENCY_CHOICES = [
        ('weekly', 'Semanal'),
        ('biweekly', 'A cada duas semanas'),
        ('monthly', 'Mensal'),
        ('2.5months', 'A cada 2.5 meses'),
        ('4months', 'A cada 4 meses'),
    ]

    name = models.CharField(max_length=255)
    beds = models.ManyToManyField(PlantBeds, blank=True, help_text="Número dos canteiros, ex: 1,2 ou 1-3")
    frequency = models.CharField(max_length=50, choices=EVENT_FREQUENCY_CHOICES)
    moon_phase = models.ForeignKey(MoonPhase, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    calendar_color = models.CharField(max_length=7, null=True, blank=True, default="#123456")

    def create_or_update_cyclic_events(self):
        eventos_pagina = EventIndexPage.objects.get(title="Plant Calendar")
        current_date = self.start_date

        delta = timedelta(weeks={
            'weekly': 1,
            'biweekly': 2,
            'monthly': 4,
            '2.5months': 10,
            '4months': 16,
        }.get(self.frequency, 1))

        if self.moon_phase:
            # Find the next occurrence of the specified lunar phase
            current_date = self.get_next_moon_phase_date(current_date)

        while current_date < datetime.now().date() + timedelta(weeks=16):
            # Check for an existing event with the same title and date
            existing_event = CyclicEventPage.objects.filter(
                title=self.name,
                occurrences__start=current_date
            ).first()

            # If an existing event is found, delete it to prevent duplication
            if existing_event:
                existing_event.delete()

            # Create or update the event with the latest details
            evento = CyclicEventPage(
                title=self.name,
                calendar_color=self.calendar_color,
                cyclic_event=self,
                first_published_at=timezone.now(),
                last_published_at=timezone.now(),
            )
            eventos_pagina.add_child(instance=evento)
            evento.occurrences.create(start=current_date, end=current_date)
            evento.save_revision().publish()

            # Adjust current_date based on moon phase or frequency
            if self.moon_phase:
                current_date = self.get_next_moon_phase_date(current_date)
            else:
                current_date += delta



    def get_next_moon_phase_date(self, start_date):
        """Retrieve the next occurrence of the selected lunar phase after the given date."""
        next_occurrence = start_date
        # Assuming MoonPhase has a related MoonPhaseEvent model with a datetime field
        while True:
            next_occurrence += timedelta(days=1)  # Check the next day
            # Get the next moon phase event after the current date
            moon_phase_event = MoonPhaseEvent.objects.filter(
                moon_phase=self.moon_phase,
                datetime__gt=next_occurrence
            ).order_by('datetime').first()
            if moon_phase_event:
                return moon_phase_event.datetime.date()

    def __str__(self):
        return str(self.name)
    
class CyclicEventPage(EventPage):
    completed = models.BooleanField(default=False)
    cyclic_event = models.ForeignKey(CyclicEvent, verbose_name=("Cyclic event"), null=True, on_delete=models.SET_NULL)
    
    # Override serve method to handle form submission
    def serve(self, request):
        if request.method == "POST":
            form = EventCompletionForm(request.POST)
            if form.is_valid():
                # Update the completed field and save
                self.completed = form.cleaned_data['completed']
                if self.completed:
                    self.calendar_color = "#088030"
                else:
                    self.calendar_color = self.cyclic_event.calendar_color
                self.save()
                return redirect('/plant-calendar/')  # Redirect back to the page after submission
        else:
            form = EventCompletionForm(initial={'completed': self.completed})

        # Render the page with the form
        return render(request, 'coderedcms/pages/cyclic_event_page.html', {
            'page': self,
            'form': form,
        })

class Note(models.Model):
    note = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.create_event()
        return super(Note, self).save(*args, **kwargs)

    def create_event(self):
        eventos_pagina = EventIndexPage.objects.get(title="Plant Calendar")
        
        # Conteúdo do evento usando RichTextBlock
        body_content = [{"type": "rich_text", "value": self.note}]
        
        evento = EventPage(
            title=f"Note - {self.date}",
            body=blocks.StreamValue(EventPage.body.field.stream_block, body_content, is_lazy=True),
            calendar_color="#eed709",
            first_published_at=timezone.now(),
            last_published_at=timezone.now(),
        )
        
        eventos_pagina.add_child(instance=evento)
        evento.occurrences.create(start=self.date, end=self.date)
        evento.save_revision().publish()
        
    def __str__(self):
        return f'Note - {self.date}'
    
class PlantBedListPage(CoderedPage):
    intro = RichTextField(blank=True)
    template = "website/plant_bed_list_page.html"
    content_panels = CoderedPage.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['plant_beds'] = PlantBeds.objects.all()
        return context