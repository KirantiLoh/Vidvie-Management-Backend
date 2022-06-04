from django.urls import path
from . import views

urlpatterns = [
    path('stocks/divisions/<slug:slug>', views.items_by_division_view, name = 'Items By Division'),
    path('stocks/<int:id>', views.item_view, name = 'Item View'),
]
