from django.urls import path
from .views import RegisterStudentAPIView, LoginAPIView, LogoutAPIView, refresh_token

urlpatterns = [
    # User Authentication Endpoints
    path('register/', RegisterStudentAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', refresh_token, name='token_refresh'),
]
