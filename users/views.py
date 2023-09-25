from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import ProfileSerializer, ProfileRetrieveSerializer, MyTokenObtainPairSerializer, \
    ShortProfileRetrieveSerializer
from users.permissions import IsProfileOwner


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования профиля пользователя"""
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsProfileOwner]

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретного профиля пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.id == self.kwargs['pk']:
            serializer_class = ProfileRetrieveSerializer
        else:
            serializer_class = ShortProfileRetrieveSerializer
        return serializer_class


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения JWT-токена"""
    serializer_class = MyTokenObtainPairSerializer
