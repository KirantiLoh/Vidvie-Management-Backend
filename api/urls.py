from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # API Routes
    path('', views.getRoutes, name='Routes'),
    path('token', views.MyTokenObtainPairView.as_view(), name = 'Login'),
    path('token/refresh', TokenRefreshView.as_view(), name = 'Refresh Token'),
    # URLs from User App
    path('divisions', views.divisions_view, name = 'Divisions'),
    path('divisions/<slug:slug>', views.division_view, name = 'Division'),

    # URLs from Task App
    path('tasks', views.tasks_view, name = 'Tasks'),
    path('tasks/<int:id>', views.task_view, name = 'Task Detail'),
    path('tasks/division/<slug:slug>', views.tasks_by_division_view, name = 'Tasks'),
    path('requests', views.requests_view, name = 'Requests'),
    path('requests/division/<slug:slug>', views.requests_by_division_view, name = 'Tasks'),

    # URLs from Item App
    path('stocks/divisions/<slug:slug>', views.items_by_division_view, name = 'Items By Division'),
    path('stocks/<int:id>', views.item_view, name = 'Item View'),
]
