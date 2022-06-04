from django.urls import path
from . import views

urlpatterns = [
    path('divisions', views.divisions_view, name = 'Divisions'),
    path('divisions/<slug:slug>', views.division_view, name = 'Division'),
]
