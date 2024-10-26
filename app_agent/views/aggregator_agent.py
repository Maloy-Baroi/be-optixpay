from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_auth.models import CustomUser
from app_agent.models.agent import AgentProfile, PaymentAggregatorAgent, PaymentProvider
from app_agent.serializers.aggregator_agent import AgentProfileSerializer, PaymentAggregatorAgentSerializer, PaymentProviderSerializer
from django.db import transaction

class CreateUserAgentProviderAPIView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Extract user data from the request
        user_data = request.data.get('user')
        agent_data = request.data.get('agent')
        providers_data = request.data.get('providers', [])  # In case it's multiple providers

        # Step 1: Create user
        user = CustomUser.objects.create(
            email=user_data['email'],
            name=user_data['name'],
            password=user_data['password']
        )

        # Step 2: Create agent profile (including handling file uploads)
        agent_serializer = AgentProfileSerializer(data=agent_data)
        if not agent_serializer.is_valid():
            return Response(agent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        agent_profile = agent_serializer.save(user=user)

        # Step 3: Create payment providers
        provider_list = []
        for provider_data in providers_data:
            provider_serializer = PaymentProviderSerializer(data=provider_data)
            if provider_serializer.is_valid():
                provider_list.append(provider_serializer.save())
            else:
                return Response(provider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Create payment aggregator agent and associate providers
        aggregator_serializer = PaymentAggregatorAgentSerializer(data={'agent_profile': agent_profile.id})
        if aggregator_serializer.is_valid():
            aggregator_agent = aggregator_serializer.save()
            aggregator_agent.providers.set(provider_list)  # Associate providers with aggregator agent
        else:
            return Response(aggregator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': {
                'email': user.email,
                'name': user.name
            },
            'agent': agent_serializer.data,
            'providers': [provider_serializer.data for provider_serializer in provider_list],
        }, status=status.HTTP_201_CREATED)
