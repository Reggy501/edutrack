from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, login_view, profile_view, logout_view

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/profile/', profile_view, name='profile'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
