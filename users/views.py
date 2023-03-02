from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.utils import Utils

from .models import AccessTypes
from .serializers import (LoginSerializer, UserAccessLogsSerializer,
                          UserSerializer)

User = get_user_model()


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                user_agent, platform, ip_address = Utils.get_request_info(
                    request
                )
                user = User.objects.filter(email=request.data.get('email'))\
                    .first()
                user_access_log_data = {
                    "user": user.id,
                    "access_type": AccessTypes.EMAIL_PASSWORD,
                    "user_agent": user_agent,
                    "platform": platform,
                    "ip_address": ip_address,
                }

                access_log_data = UserAccessLogsSerializer(
                    data=user_access_log_data
                )
                if access_log_data.is_valid():
                    access_log_data.save()
                else:
                    return Response(
                        access_log_data.errors,
                        status.HTTP_400_BAD_REQUEST
                    )
            return response
        except InvalidToken as e:
            raise e


class UserView(ModelViewSet):   # pylint: disable=R0901
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    # Changes default lookup field for details endpoints
    lookup_field = 'public_id'
