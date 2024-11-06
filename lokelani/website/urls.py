from django.urls import path
from website import views


urlpatterns = [
path('plant-beds/<int:bed_id>/', views.plant_bed, name='plant_bed_page'),
path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]


