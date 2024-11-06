from django.contrib import admin
from website.models import MoonPhase, MoonPhaseEvent, CyclicEventPage, CyclicEvent, PlantBeds, Plantation, Plant, Note
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

@admin.register(MoonPhase)
class Admin(admin.ModelAdmin):
    pass

@admin.register(MoonPhaseEvent)
class MoonPhaseEventAdmin(admin.ModelAdmin):
    pass

class InlineCycleEventPage(admin.StackedInline):
    model = CyclicEventPage
    extra = 0
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Assuming `occurrences` is a related field and `start_date` is the date field.
        # Use `occurrences__start` to access the `start` field in related `occurrences`.
        return qs.filter(occurrences__start=request.GET.get('start_date', None))
    
@admin.register(CyclicEvent)
class CyclicEventAdmin(admin.ModelAdmin):
    filter_horizontal =['beds']
    inlines = [InlineCycleEventPage]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.create_or_update_cyclic_events()
        
    def delete_model(self, request, obj):
        # Delete all associated CyclicEventPages before deleting the CyclicEvent
        try:
            # Get all pages associated with this CyclicEvent
            cyclic_event_pages = CyclicEventPage.objects.filter(cyclic_event=obj)
            for page in cyclic_event_pages:
                page.delete()  # This will call the delete method for the page, including any related objects
        except ObjectDoesNotExist:
            # Handle the case where no pages are found, if needed
            pass
        
        # Now call the super method to delete the CyclicEvent itself
        super().delete_model(request, obj)
@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    pass

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_filter = ['date', 'bed']
    list_display = ['note', 'date', 'bed']
    
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('/plant-calendar')

    def response_change(self, request, obj):
        return HttpResponseRedirect('/plant-calendar')
   
class PlantationInline(admin.TabularInline):
    model = Plantation
    extra = 1        
@admin.register(PlantBeds)
class PlantBedsAdmin(admin.ModelAdmin):
    inlines = [PlantationInline]
