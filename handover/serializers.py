from asyncore import read
from typing import ItemsView
from rest_framework import serializers
from .models import HandOver
from item.serializers import ItemSerializer

class HandoverSerializer(serializers.ModelSerializer):
    requestor = serializers.StringRelatedField()
    requestor_division = serializers.StringRelatedField()
    requestee_division = serializers.StringRelatedField()
    item = ItemSerializer(read_only = True, many = False)
    class Meta:
        model = HandOver
        fields = '__all__'