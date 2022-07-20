from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # API Routes
    path('', views.getRoutes, name='Routes'),
    path('token', views.MyTokenObtainPairView.as_view(), name = 'Login'),
    path('token/refresh', TokenRefreshView.as_view(), name = 'Refresh Token'),
    # URLs from User App
    path('', include('user.urls')),

    # URLs from Task App
    path('', include('task.urls')),
    
    # URLs from Item App
    path('', include('item.urls')),

    #URLs from Handover App
    path('', include('handover.urls')),
]
