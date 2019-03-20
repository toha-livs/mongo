from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_authenticated', 'is_active', 'email', 'first_name', 'last_name', 'is_anonymous')
