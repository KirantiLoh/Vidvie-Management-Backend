from dateutil import parser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from user.models import Account, Division
from task.models import Task
from task.serializers import TaskSerializer
from task.filters import TaskFilter

# Create your views here.
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
        division = account.division
        if request.method == 'POST':
            data = request.data
            try:
                task = Task.objects.get(id = id)
                if division == task.requestor_division or division == task.requestee_division:
                    requestor = Division.objects.get(name=data['requestor_division'])
                    requestee = Division.objects.get(name=data['requestee_division'])
                    if task.title == data['title'] and task.description == data['description'] and task.priority == data['priority'] and task.status == data['status'] and task.deadline == parser.parse(data['deadline']) and task.requestor_division == requestor and task.requestee_division == requestee:
                        return Response({"message": "No data was changed"}, status=status.HTTP_400_BAD_REQUEST)
                    task.title = data['title']
                    task.description = data['description']
                    task.priority = data['priority']
                    task.status = data['status']
                    task.deadline = parser.parse(data['deadline'])
                    task.requestor_division = requestor
                    task.requestee_division = requestee
                    task.save()
                    return Response({'message': 'Task successfully updated'}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "You are not allowed to update this task!"}, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                return Response({'message': 'Task cannot be updated due to some error...', status: status.HTTP_400_BAD_REQUEST})
        if request.method == 'DELETE':
            task = Task.objects.get(id=id)
            if division == task.requestor_division or division == task.requestee_division:
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
        paginator.page_size = 10
        tasks = TaskFilter(request.GET, Task.objects.all()).qs
        result = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result, many = True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        data = request.data
        deadline = parser.parse(data['deadline'])
        try:
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
            return Response({"message": "Request successfully created!"}, status = status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"message": "Requestee division or requestor division does not exist"}, status = status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks_by_division_view(request, slug):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 7
        try:
            division = Division.objects.get(slug=slug)
            tasks_by_division = TaskFilter(request.GET, division.tasks.all()).qs
            result = paginator.paginate_queryset(tasks_by_division, request)
            serializer = TaskSerializer(result, many = True)
            return paginator.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"message": "Division does not exist..."}, status = status.HTTP_404_NOT_FOUND)
   

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
