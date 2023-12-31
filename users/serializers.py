from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.serializers import PaymentSerializer
from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля"""

    class Meta:
        model = User
        fields = '__all__'


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля"""
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'city', 'payments']


class ShortProfileRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля: сокращенная версия для не владельца"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'phone', 'city']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для обработки запросов на получение токена"""

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        return token
