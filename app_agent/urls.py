from django.urls import path

from app_agent.views.aggregator_agent import CreateUserAgentProviderAPIView, AgentProfileListView
from app_agent.views.payment_provider import PaymentProviderListCreateAPIView, PaymentProviderDetailAPIView

urlpatterns = [
    path('agents/', AgentProfileListView.as_view(), name='payment-provider-list-create'),
    path('payment-providers/', PaymentProviderListCreateAPIView.as_view(), name='payment-provider-list-create'),
    path('payment-providers/<int:pk>/', PaymentProviderDetailAPIView.as_view(), name='payment-provider-detail'),
    path('create-user-agent-provider/', CreateUserAgentProviderAPIView.as_view(), name='create_user_agent_provider'),
]
