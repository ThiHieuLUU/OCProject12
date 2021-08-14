"""Views login process of a user."""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserLoginSerializer,
)


class UserLoginView(GenericAPIView):
    """Views for login process."""

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User logged in successfully',
            'access': serializer.data['access'],
            'refresh': serializer.data['refresh'],
            'authenticatedUser': {
                'username': serializer.data['username'],
            }
        }

        return Response(response, status=status_code)


class BlacklistTokenUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successful logout", status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response("Refresh token is invalid or is blacklisted", status=status.HTTP_400_BAD_REQUEST)

