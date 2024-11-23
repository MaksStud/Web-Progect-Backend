import logging

from rest_framework import serializers
from rest_framework import status

from .models import User


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = email
            user.set_password(password)
            user.save()
            attrs['user'] = user
        elif not created and user.check_password(password):
            attrs['user'] = user
        else:
            raise serializers.ValidationError(detail='Email or password is incorrect.', code=status.HTTP_403_FORBIDDEN)

        return attrs

    def create(self, validated_data):
        return validated_data.get('user')

