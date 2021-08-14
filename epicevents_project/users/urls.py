from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from rest_auth.views import (
    LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

from .views import (
    UserLoginView,
    # UserLogoutView,
    BlacklistTokenUpdateView
)

app_name = "users"


urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('account/logout/', UserLogoutView.as_view(), name='logout'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),

    # Include the endpoints from rest_auth
    # URLs that require a user to be logged in with a valid session / token.
    path('account/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),  # Ok
    path('account/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('account/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # path('account/logout/', LogoutView.as_view(), name='rest_logout'),  # Work but after can get data, e.g: /lists/
]
