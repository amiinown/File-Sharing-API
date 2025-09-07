from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, ResetPasswordRequest, ResetPasswordConfirm



app_name = 'accounts'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('reset-password/request/', ResetPasswordRequest.as_view(), name='reset-password-request'),
    path('reset-password/confirm/', ResetPasswordConfirm.as_view(), name='reset-password-confirm'),
]