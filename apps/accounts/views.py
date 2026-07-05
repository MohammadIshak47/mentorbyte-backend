from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — public signup endpoint."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ — returns access/refresh tokens + user profile."""

    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me/ — the logged-in user's own profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
