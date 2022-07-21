from asyncio import exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import HandOver
from .serializers import HandoverSerializer
from user.models import Account, Division
from item.models import Item
from .filters import HandOverFilter
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def handovers_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        handovers = HandOverFilter(request.GET, HandOver.objects.all()).qs
        result = paginator.paginate_queryset(handovers, request)
        serializer = HandoverSerializer(result, many = True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        data = request.data
        try:
            count = int(data['count'])
            requestor = Account.objects.get(user__username = data['requestor'])
            requestor_division = Division.objects.get(name = data['requestor_division'])
            requestee_division = Division.objects.get(name = data['requestee_division'])
            item = Item.objects.get(name = data['item'])
            if item.stock < count:
                return Response({"message":"The amount of items wanted requested is greater than the stock"}, status = status.HTTP_400_BAD_REQUEST)
            if data['tipe'] == 'Pengembalian' and item.borrowed < count:
                return Response({"message":"The amount of items wanted to be returned is greater than the borrowed amount"}, status = status.HTTP_400_BAD_REQUEST)
            if requestor.division != requestor_division:
                return Response({"message":'The requesting user is not from the inputed requesting division'}, status = status.HTTP_400_BAD_REQUEST)
            if item.division != requestee_division:
                return Response({"message":'The requested item is not from the inputed requested division'}, status = status.HTTP_400_BAD_REQUEST)
            if requestor_division == requestee_division:
                return Response({"message":'You cannot borrow items from your own division'}, status = status.HTTP_400_BAD_REQUEST)
            HandOver.objects.create(
                tipe = data['tipe'],
                item = item,
                requestor_division = requestor_division,
                requestee_division = requestee_division,
                requestor = requestor,
                description = data['description'],
                count = count,
            )
            if (data['tipe'] == 'Peminjaman'): 
                item.stock -= count
                item.borrowed += count
            elif(data['tipe'] == 'Permintaan'):
                item.stock -= count
            else:
                item.stock += count
                item.borrowed -= count
            item.save()
            return Response({"message": "Form created successfully!"}, status = status.HTTP_201_CREATED)
        except (KeyError, TypeError, ObjectDoesNotExist):
            return Response({"message": "Invalid arguments in the request"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handovers_by_division_view(request, division):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        handovers = HandOverFilter(request.GET, HandOver.objects.filter(requestor_division__slug=division)).qs
        result = paginator.paginate_queryset(handovers, request)
        serializer = HandoverSerializer(result, many = True)
        return paginator.get_paginated_response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def handover_view(request, id):
    try:
        handover = HandOver.objects.get(id=id)
        if (request.method == 'GET'):
            serializer = HandoverSerializer(handover, many = False)
            return Response(serializer.data, status = status.HTTP_200_OK)
        account = Account.objects.get(user = request.user)
        if (account.division == handover.requestor_division):
            if (request.method == 'POST'):
                data = request.data
                if (data['is_approved'] == 'true'):
                    handover.is_approved = True
                else:
                    handover.is_approved = False
                handover.save()
                return Response({"message":"Handover edited successfully"}, status = status.HTTP_200_OK)

            # if (request.method == 'DELETE'):
            #     handover.delete()
            #     return Response({"message":"Handover deleted successfully"}, status = status.HTTP_200_OK)
        return Response({"message":"You're not authorized to edit this handover"}, status=status.HTTP_400_BAD_REQUEST)
    except (KeyError, ObjectDoesNotExist):
        return Response({"message": "Invalid arguments in the request"}, status = status.HTTP_400_BAD_REQUEST)