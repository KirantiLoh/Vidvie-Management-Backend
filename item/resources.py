from .models import Item
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from user.models import Division

class ItemResource(resources.ModelResource):
    division = fields.Field(column_name='division', attribute='division', widget=ForeignKeyWidget(Division, field='name'))
    class Meta:
        model = Item
        import_id_fields =('name',)
        fields = (
            'name',
            'function',
            'condition',
            'stock',
            'division',
            'date_added',
            'date_updated',
        )