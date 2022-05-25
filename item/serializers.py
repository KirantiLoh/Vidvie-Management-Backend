from rest_framework import serializers
from .models import Item
from user.serializers import DivisionSerializer

class ItemSerializer(serializers.ModelSerializer):
    division = DivisionSerializer(read_only=True, many = False)
    class Meta:
        model = Item
        fields = ('id', 'name', 'stock', 'function', 'condition', 'division', 'date_added', 'date_updated')
