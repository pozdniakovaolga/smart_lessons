from django.urls import path

from users.apps import UsersConfig
from users.views import ProfileUpdateAPIView, ProfileRetrieveAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('profile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_get'),
    path('profile/update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile'),
]
