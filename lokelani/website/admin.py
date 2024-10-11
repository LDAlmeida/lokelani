from django.contrib import admin
from website.models import MoonPhase, MoonPhaseEvent, CyclicEventPage, CyclicEvent, PlantBeds

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
        obj.create_cyclic_events()
        
@admin.register(PlantBeds)
class PlantBedsAdmin(admin.ModelAdmin):
    pass
