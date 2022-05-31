from .models import Task
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from user.models import Division

class TaskResource(resources.ModelResource):
    requestee_division = fields.Field(column_name='requestee_division', attribute='requestee_division', widget=ForeignKeyWidget(Division, field='name'))
    requestor_division = fields.Field(column_name='requestor_division', attribute='requestor_division', widget=ForeignKeyWidget(Division, field='name'))
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'priority',
            'status',
            'date_added',
            'date_updated',
            'deadline',
            'requestor_division',
            'requestee_division',
        )
