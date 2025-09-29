from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MeView, UserListView, UserRoleUpdateView

urlpatterns = [
    # AUTH
    path('auth/login',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair_slash'),
    path('auth/refresh',  TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh_slash'),
    path('auth/me',  MeView.as_view(), name='me'),
    path('auth/me/', MeView.as_view(), name='me_slash'),

    # USERS (solo ADMIN)
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/role', UserRoleUpdateView.as_view(), name='users-role'),
]
