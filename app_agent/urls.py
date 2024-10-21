from django.urls import path

from app_agent.views.aggregator_agent import CreateUserAgentProviderAPIView

urlpatterns = [
    path('create-user-agent-provider/', CreateUserAgentProviderAPIView.as_view(), name='create_user_agent_provider'),
]
