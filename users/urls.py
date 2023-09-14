from django.urls import path

from users.apps import UsersConfig
from users.views import ProfileUpdateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('profile/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile'),
]
