from rest_framework import serializers
from .models import SecureDropUser

class SecureDropUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureDropUser
        fields = ["name", "email", "passwd", "pubkey"]

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureDropUser
        fields = ["name", "email", "pubkey"]