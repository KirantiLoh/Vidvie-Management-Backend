import re
from dateutil import parser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination

from user.serializers import AccountSerializer, DivisionSerializer
from item.serializers import ItemSerializer
from .serializers import MyTokenObtainPairSerializer
from user.models import Account, Division
from task.models import Task
from task.serializers import TaskSerializer
from task.filters import TaskFilter
from item.models import Item

from api import serializers

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
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_view(request, id):
    account = Account.objects.get(user = request.user)
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, many = False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
    try:
        division = Division.objects.get(leader = account)
        if request.method == 'POST':
            data = request.data
            try:
                task = Task.objects.get(id = id)
                requestor = Division.objects.get(name=data['requestor_division'])
                requestee = Division.objects.get(name=data['requestee_division'])
                task.title = data['title']
                task.description = data['description']
                task.priority = data['priority']
                task.status = data['status']
                task.deadline = parser.parse(data['deadline'])
                task.requestor_division = requestor
                task.requestee_division = requestee
                task.save()
                return Response({'message': 'Task successfully updated'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'message': 'Task cannot be updated due to some error...', status: status.HTTP_400_BAD_REQUEST})
        if request.method == 'DELETE':
            task = Task.objects.get(id=id)
            if task.requestor_division == division:
                task.delete()
                return Response({'message': 'Task successfully deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "You are not allowed to delete this task!"}, status=status.HTTP_403_FORBIDDEN)       
    except ObjectDoesNotExist:
        return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)       

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 5
        tasks = TaskFilter(request.GET, Task.objects.all()).qs
        result = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result, many = True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        data = request.data
        deadline = parser.parse(data['deadline'])
        requestor_division = Division.objects.get(name = data['requestor_division'])
        requestee_division = Division.objects.get(name = data['requestee_division'])
        task = Task.objects.create(
            title = data['title'],
            description = data['description'],
            priority = data['priority'],
            status = data['status'],
            deadline = deadline,
            requestee_division = requestee_division,
            requestor_division = requestor_division
        )
        task.save()
        return Response({"message": "Request successfully created!"}, status = status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 3
        division = Account.objects.get(user = request.user).division
        requests = TaskFilter(request.GET, division.requests.all()).qs
        result = paginator.paginate_queryset(requests, request)
        serializer = TaskSerializer(result, many = True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def tasks_by_division_view(request, slug):
    account = Account.objects.get(user = request.user)
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 3
        try:
            division = Division.objects.get(slug=slug)
            tasks_by_division = TaskFilter(request.GET, division.tasks.all()).qs
            result = paginator.paginate_queryset(tasks_by_division, request)
            serializer = TaskSerializer(result, many = True)
            return paginator.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"message": "Division does not exist..."}, status = status.HTTP_404_NOT_FOUND)
    try:
        division = Division.objects.get(leader = account)
        if request.method == 'PATCH':
            data = request.data
            if data['updating'] == 'Status':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.status = data['updatedValue']
                        task.save()
                    else:
                        pass
            if data['updating'] == 'Deadline':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.deadline = parser.parse(data['updatedValue'])
                        task.save()
                    else:
                        pass
            if data['updating'] == 'Priority':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.priority = data['updatedValue']
                        task.save()
                    else:
                        pass
            return Response({"message": "Tasks Successfully updated"}, status = status.HTTP_200_OK)            
        if request.method == 'DELETE':
            data = request.data['data']
            for id in data['isChecked']:
                task = Task.objects.get(id=id)
                if task.requestor_division == division:
                    task.delete()
                    return Response({"message": "Tasks Successfully deleted"}, status = status.HTTP_200_OK)  
                else:
                    return Response({"message": "This task can't be deleted because you're not the requestor"}, status=status.HTTP_403_FORBIDDEN)              
    except ObjectDoesNotExist:
        return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)              

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def requests_by_division_view(request, slug):
    account = Account.objects.get(user = request.user)
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 3
        try:
            division = Division.objects.get(slug=slug)
            requests_by_division = TaskFilter(request.GET, division.requests.all()).qs
            result = paginator.paginate_queryset(requests_by_division, request)
            serializer = TaskSerializer(result, many = True)
            return paginator.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"message": "Division does not exist..."}, status = status.HTTP_404_NOT_FOUND)
    try:
        division = Division.objects.get(leader = account)
        if request.method == 'PATCH':
            data = request.data
            if data['updating'] == 'Status':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.status = data['updatedValue']
                        task.save()
                    else:
                        pass
            if data['updating'] == 'Deadline':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.deadline = parser.parse(data['updatedValue'])
                        task.save()
                    else:
                        pass
            if data['updating'] == 'Priority':
                for id in data['isChecked']:
                    task = Task.objects.get(id=id)
                    if task.requestor_division == division:
                        task.priority = data['updatedValue']
                        task.save()
                    else:
                        pass
            return Response({"message": "Tasks Successfully updated"}, status = status.HTTP_200_OK)            

        if request.method == 'DELETE':
            data = request.data
            for id in data['isChecked']:
                request = Task.objects.get(id=id)
                if request.requestor_division == division:
                    request.delete()
                    return Response({"message": "Tasks Successfully deleted"}, status = status.HTTP_200_OK)  
                else:
                    return Response({"message": "This task can't be deleted because you're not the requestor"}, status=status.HTTP_403_FORBIDDEN)              
    except ObjectDoesNotExist:
        return Response({"message": "You are not allowed to do any modification!"}, status=status.HTTP_403_FORBIDDEN)     

@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def items_by_division_view(request, slug):
    account = Account.objects.get(user = request.user)
    try:
        division = Division.objects.get(slug=slug)
        if request.method == 'GET':
            paginator = PageNumberPagination()
            paginator.page_size = 10
            items = division.items.all()
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
            if request.method == 'PATCH':
                data = request.data
                if data['updating'] == 'Condition':
                    for id in data['isChecked']:
                        item = Item.objects.get(id=id)
                        if item.division == division:
                            item.condition = data['updatedValue']
                            item.save()
                        else:
                            pass
                if data['updating'] == 'Stock':
                    for id in data['isChecked']:
                        item = Item.objects.get(id=id)
                        if item.division == division:
                            item.stock = data['updatedValue']
                            item.save()
                        else:
                            pass
                return Response({"message": "Items successfully updated"}, status=status.HTTP_200_OK)
            if request.method == 'DELETE':
                data = request.data
                for id in data['isChecked']:
                    item = Item.objects.get(id=id)
                    item.delete()
                return Response({"message": "Items successfully deleted"}, status=status.HTTP_200_OK)
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
            serializer = ItemSerializer(item, many = False)
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
