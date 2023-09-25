from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import ProfileSerializer, ProfileRetrieveSerializer, MyTokenObtainPairSerializer


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования профиля пользователя"""
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(User, pk=pk)
        return obj


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретного профиля пользователя"""
    serializer_class = ProfileRetrieveSerializer
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения JWT-токена"""
    serializer_class = MyTokenObtainPairSerializer
