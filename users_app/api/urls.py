from django.urls import path
from .views import RegistrationView, ActivateAccountView, PasswordResetConfirmView, PasswordResetRequestView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Registrierung & Aktivierung
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='user-activate'),

    # Authentifizierung (JWT)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Passwort reset
    path('reset-password/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


