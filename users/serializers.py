from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Пользователь"""

    class Meta:
        model = User
        fields = '__all__'
