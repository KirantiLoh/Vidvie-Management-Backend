from user.models import Account, Division
from item.models import Item
from item.filters import ItemFilter
from item.serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def items_by_division_view(request, slug):
    account = Account.objects.get(user = request.user)
    try:
        division = Division.objects.get(slug=slug)
        if request.method == 'GET':
            paginator = PageNumberPagination()
            paginator.page_size = 10
            items = ItemFilter(request.GET, division.items.all()).qs
            result = paginator.paginate_queryset(items, request)
            serializer = ItemSerializer(result, many = True)
            return paginator.get_paginated_response(serializer.data)
        if division.leader == account:
            if request.method == 'POST':
                data = request.data
                item = Item.objects.create(
                    name=data['name'],
                    stock=data['stock'],
                    condition=data['condition'],
                    function= data['function'],
                    division=division
                )
                item.save()
                return Response({'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)     
    except ObjectDoesNotExist:
        return Response({"message": "Division does not exist..."}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def item_view(request, id):
    account = Account.objects.get(user=request.user)
    try:
        item = Item.objects.get(id=id)
        if request.method == 'GET':
            serializer = ItemSerializer(item.history.all(), many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if (item.division.leader == account):
            if request.method == 'POST':
                data = request.data
                item.name = data['name']
                item.condition = data['condition']
                item.stock = data['stock']
                item.function = data['function']
                item.save()
                return Response({"message": "Item saved successfully"})
            if request.method == 'DELETE':
                item.delete()
                return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)     
    except ObjectDoesNotExist:
        return Response({"message": "Item does not exist"}, status = status.HTTP_404_NOT_FOUND)
