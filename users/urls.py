from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from users.views import ProfileUpdateAPIView, ProfileRetrieveAPIView, MyTokenObtainPairView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('profile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_get'),
    path('profile/update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
