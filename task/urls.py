from django.urls import path
from . import views

urlpatterns = [
    path('tasks', views.tasks_view, name = 'Tasks'),
    path('tasks/<int:id>', views.task_view, name = 'Task Detail'),
    path('tasks/division/<slug:slug>', views.tasks_by_division_view, name = 'Tasks'),
    path('requests', views.requests_view, name = 'Requests'),
    path('requests/division/<slug:slug>', views.requests_by_division_view, name = 'Tasks'),

]
