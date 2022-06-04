from dateutil import parser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = {
        'account',
        'tasks',
        'tasks/division/<slug:slug>',
        'divisions',
        'divisions/<slug:slug>',
        'token',
        'token/refresh'
    }
    return Response(routes, status = status.HTTP_200_OK)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


