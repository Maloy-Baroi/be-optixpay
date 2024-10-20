from django.urls import path

from app_auth.views.create_user import VerifyOTPView, CustomUserCreateView
from app_auth.views.users import CustomTokenObtainPairView, CustomTokenRefreshView
from app_auth.views.agent_profile import (
    AgentProfileCreateAPI,
    AgentProfileRetrieveAPIView,
    AgentProfileUpdateAPIView
)
from app_auth.views.wallet import WalletViewSet

wallet_list = WalletViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

wallet_detail = WalletViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

app_name = 'app_auth'

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='user-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('login/token/refresh/', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),

    path('agent-profile/create/', AgentProfileCreateAPI.as_view(), name='agent-profile-create'),
    path('agent-profile/<int:pk>/', AgentProfileRetrieveAPIView.as_view(), name='agent-profile-retrieve'),
    path('agent-profile/<int:pk>/update/', AgentProfileUpdateAPIView.as_view(), name='agent-profile-update'),
    path('wallets/', wallet_list, name='wallet-list'),
    path('wallets/<int:pk>/', wallet_detail, name='wallet-detail'),
]
