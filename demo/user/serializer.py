import json
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, CharField, ModelSerializer, \
    BooleanField, ValidationError, EmailField, IntegerField, SerializerMethodField, ListSerializer
from .models import UserProfile
from demo.exceptions import ErrorEnum
class CreateUserPayloadSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)
    email = EmailField(required=True)

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise ValidationError(code=ErrorEnum.USERNAME_IS_EXISTS)
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError(code=ErrorEnum.EMAIL_IS_EXISTS)
        return data