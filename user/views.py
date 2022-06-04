from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from user.serializers import AccountSerializer, DivisionSerializer
from user.models import Account, Division
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def divisions_view(request):
    if request.method == 'GET':
        divisions = Division.objects.all()
        serializer = DivisionSerializer(divisions, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def division_view(request, slug):
    if request.method == 'GET':
        try:
            division = Division.objects.get(slug = slug)
            division_serializer = DivisionSerializer(division, many = False)
            result = division_serializer.data
            members = division.members.all()
            account_serializer = AccountSerializer(members, many = True)
            result['members'] = account_serializer.data
            return Response(result, status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Division does not exist..."}, status = status.HTTP_404_NOT_FOUND)
    