from rest_framework import serializers
from task.models import Task
from user.serializers import DivisionSerializer

class TaskSerializer(serializers.ModelSerializer):
    requestee_division = DivisionSerializer(many = False, read_only = True)
    requestor_division = DivisionSerializer(many = False, read_only = True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority', 'status', 'date_added', 'date_updated', 'deadline', 'requestor_division', 'requestee_division')