from django.urls import path
from . import views

urlpatterns = [
    path('handovers', views.handovers_view, name = 'Handovers View'),
    path('handovers/division/<str:division>', views.handovers_by_division_view, name = 'Handovers View'),
    path('handovers/<int:id>', views.handover_view, name = 'Handover View'),
]
