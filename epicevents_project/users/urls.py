from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from rest_auth.views import (
    LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

from .views import (
    UserLoginView
)

app_name = "users"


urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginView.as_view(), name='login'),
]
