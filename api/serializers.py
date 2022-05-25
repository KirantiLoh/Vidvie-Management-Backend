from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import Account
from django.core.exceptions import ObjectDoesNotExist

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        account = Account.objects.get(user=user)
        token['username'] = user.username
        token['name'] = f"{user.first_name} {user.last_name}"
        token['division'] = account.division.name
        try:
            if (user.username == account.division.leader.user.username):
                token['leader_of'] = account.division.name
        except ObjectDoesNotExist:
            pass
        return token