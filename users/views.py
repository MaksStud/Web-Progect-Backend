from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthUserSerializer


class AuthUserViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = AuthUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')

        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        return Response(tokens, status=status.HTTP_200_OK)


