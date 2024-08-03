from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from authentification.serializers import UserSerializer
from authentification.models import User

import logging


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logger = logging.getLogger(__name__)
        try:
            refresh_token = request.data["refresh_token"]
            logger.debug(f"Received refresh token: {refresh_token}")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        logger = logging.getLogger(__name__)
        email = request.data.get('email')
        logger.debug(f"Login attempt for email: {email}")

        if email is None:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            logger.debug(f"User found: {user}")
        except User.DoesNotExist:
            logger.warning(f"Invalid credentials for email: {email}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        logger.debug(f"Tokens created: Access: {refresh.access_token}, Refresh: {refresh}")
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
