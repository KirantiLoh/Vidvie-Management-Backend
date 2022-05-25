from rest_framework import serializers
from .models import Account, Division
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(many = False, read_only = True)
    division = serializers.StringRelatedField(many = False)
    class Meta:
        model = Account
        fields = ('id', 'user', 'division')

class DivisionSerializer(serializers.ModelSerializer):
    leader = AccountSerializer(many = False, read_only = True)
    class Meta:
        model = Division
        fields = ('id', 'name', 'leader', 'slug', 'whatsapp_number')