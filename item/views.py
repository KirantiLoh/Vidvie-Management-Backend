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
from PIL import Image

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
                try:
                    if (int(data['stock']) < 0):
                        return Response({"message": "Stock cannot be negative"}, status = status.HTTP_400_BAD_REQUEST)
                    if (data.get('image')):
                        try:
                            img = Image.open(data['image'])
                            img.verify()
                            Item.objects.create(
                                image=data['image'],
                                name=data['name'],
                                stock= int(data['stock']),
                                condition=data['condition'],
                                function= data['function'],
                                division=division
                            )
                            return Response({'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
                        except:
                            return Response({"message": "Image must be either a jpeg or png"}, status = status.HTTP_400_BAD_REQUEST)
                    else:
                        Item.objects.create(
                                name=data['name'],
                                stock= int(data['stock']),
                                condition=data['condition'],
                                function= data['function'],
                                division=division
                            )
                    return Response({'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
                except ValueError:
                    return Response({"message": "Stock must be a number"}, status = status.HTTP_400_BAD_REQUEST)
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
                try:
                    stock = int(data['stock'])
                    broken = int(data['broken'])
                    if item.name == data['name'] and item.condition == data['condition'] and item.stock == stock and item.broken == broken and item.function == data['function'] and not data.get("image"):
                        return Response({"message":"No data was changed"}, status=status.HTTP_400_BAD_REQUEST)
                    if (stock < 0 or broken < 0):
                        return Response({"message": "Stock and broken cannot be negative"}, status = status.HTTP_400_BAD_REQUEST)
                    if (stock + (item.broken - broken) < 0):
                        return Response({"message": "The amount of broken items cannot be bigger than the stock"}, status = status.HTTP_400_BAD_REQUEST)
                    item.name = data['name']
                    item.condition = data['condition']
                    item.stock = stock + (item.broken - broken)
                    item.broken = broken
                    item.function = data['function']
                    if data.get('image'):
                        item.image = data.get('image')
                    item.save()
                    return Response({"message": "Item saved successfully"})
                except ValueError:
                    return Response({"message": "Stock and broken must be a number"}, status = status.HTTP_400_BAD_REQUEST)
            if request.method == 'DELETE':
                item.delete()
                return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)     
    except ObjectDoesNotExist:
        return Response({"message": "Item does not exist"}, status = status.HTTP_404_NOT_FOUND)
