from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_auth.models import CustomUser
from app_agent.models.agent import AgentProfile, PaymentAggregatorAgent, PaymentProvider
from app_agent.serializers.aggregator_agent import AgentProfileSerializer, PaymentAggregatorAgentSerializer, \
    PaymentProviderSerializer, AgentProfileListSerializer
from django.db import transaction

# class CreateUserAgentProviderAPIView(APIView):
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         # Extract user data from the request
#         user_data = request.data.get('user')
#         agent_data = request.data.get('agent')
#         providers_data = request.data.get('providers', [])  # In case it's multiple providers
#         # providers_data = [1, 2, 5, 8,] the ids of PaymentProvider Model
#
#         # Step 1: Create user
#         user = CustomUser.objects.create(
#             email=user_data['email'],
#             name=user_data['name'],
#             password=user_data['password']
#         )
#
#         # Step 2: Create agent profile (including handling file uploads)
#         agent_serializer = AgentProfileSerializer(data=agent_data)
#         if not agent_serializer.is_valid():
#             return Response(agent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         agent_profile = agent_serializer.save(user=user)
#
#         # Step 3: Create payment providers
#         provider_list = []
#         for provider_data in providers_data:
#             provider_serializer = PaymentProviderSerializer(data=provider_data)
#             if provider_serializer.is_valid():
#                 provider_list.append(provider_serializer.save())
#             else:
#                 return Response(provider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # Step 4: Create payment aggregator agent and associate providers
#         aggregator_serializer = PaymentAggregatorAgentSerializer(data={'agent_profile': agent_profile.id})
#         if aggregator_serializer.is_valid():
#             aggregator_agent = aggregator_serializer.save()
#             aggregator_agent.providers.set(provider_list)  # Associate providers with aggregator agent
#         else:
#             return Response(aggregator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({
#             'user': {
#                 'email': user.email,
#                 'name': user.name
#             },
#             'agent': agent_serializer.data,
#             'providers': [provider_serializer.data for provider_serializer in provider_list],
#         }, status=status.HTTP_201_CREATED)


class CreateUserAgentProviderAPIView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        agent_data = request.data.get('agent')
        providers_ids = request.data.get('providers', [])  # IDs of existing PaymentProvider

        # Step 1: Create the user instance
        user = CustomUser(
            email=user_data['email'],
            name=user_data['username'],
        )
        user.set_password(user_data['password'])  # Hash the password

        # Step 2: Save the user to generate an ID
        user.save()

        # Step 3: Retrieve the 'agent' group and add the user to it
        agent_group, created = Group.objects.get_or_create(name='agent')
        user.groups.add(agent_group)

        agent_serializer = AgentProfileSerializer(data=agent_data)
        if not agent_serializer.is_valid():
            return Response(agent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        agent_profile = agent_serializer.save(user=user)

        providers = PaymentProvider.objects.filter(id__in=providers_ids)
        if not providers:
            return Response({'error': 'One or more providers not found'}, status=status.HTTP_404_NOT_FOUND)

        aggregator_agent = PaymentAggregatorAgent.objects.create(agent_profile=agent_profile)
        aggregator_agent.providers.set(providers)

        return Response({
            'user': {'email': user.email, 'name': user.name},
            'agent': agent_serializer.data,
            'providers': [provider.id for provider in providers],
        }, status=status.HTTP_201_CREATED)


class AgentProfileListView(APIView):
    def get(self, request):
        try:
            profiles = AgentProfile.objects.all()
            serializer = AgentProfileListSerializer(profiles, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
