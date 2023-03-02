# pylint: disable=W0223
from copy import copy

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserAccessLogs

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        required=True,
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        required=True,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # Try to authenticate user using Django auth framework
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError(
                _("Access denied: wrong email and password"),
                code="no_active_account"
            )
        refresh = RefreshToken.for_user(user)
        pair_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return pair_token


class UserAccessLogsSerializer(serializers.ModelSerializer):
    access_timestamp = serializers.DateTimeField(
        read_only=True
    )

    class Meta:
        model = UserAccessLogs
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    public_id = serializers.CharField(
        read_only=True
    )
    access_logs = UserAccessLogsSerializer(
        many=True,
        read_only=True
    )
    password = serializers.CharField(
        required=True,
        write_only=True
    )
    password_confirmation = serializers.CharField(
        required=True,
        write_only=True
    )

    def create(self, validated_data):
        # Validates whether matching passwords
        # were given or not
        if validated_data['password'] != validated_data[
            'password_confirmation'
        ]:
            # Raises a validation error
            raise serializers.ValidationError(
                {'password': "Passwords must be equal"}
            )
        # Makes a copy for the validated
        # data payload
        user_data = copy(validated_data)
        # Removes passwords keys
        user_data.pop('password')
        user_data.pop('password_confirmation')
        user = User(**user_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        exclude = (
            "id",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "is_active"
        )
        extra_kwargs = {
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }
