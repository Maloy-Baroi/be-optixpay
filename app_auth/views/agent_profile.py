from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from app_auth.models.agent_profile import AgentProfile
from app_auth.serializers.agent_profile import (
    AgentProfileCreateSerializer,
    AgentProfileUpdateSerializer,
    AgentProfileRetrieveSerializer
)
from drf_yasg.utils import swagger_auto_schema
import uuid
from django.utils.timezone import now
from services.minio_storage import upload_file_to_minio


def generate_unique_filename(original_filename):
    # Generate a unique identifier
    unique_id = str(uuid.uuid4())[:10]
    # Extract the file extension by splitting from the last dot
    parts = original_filename.rsplit('.', 1)
    if len(parts) == 2:
        # File has an extension
        name, extension = parts
        extension = f".{extension}"  # Re-add the dot
    else:
        # No extension
        name, extension = parts[0], ''

    # Generate a unique file name
    unique_filename = f"{name}_{now().strftime('%Y%m%d%H%M%S')}_{unique_id}{extension}"
    return unique_filename


class AgentProfileCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Initialize a dictionary to hold potential file data
        uploaded_files = {}
        print(request.FILES.get('front_side_document'))
        print(request.FILES.get('back_side_document'))

        # Check for both 'front_side_document' and 'back_side_document' in the uploaded files
        for field_name in ['front_side_document', 'back_side_document']:
            file_obj = request.FILES.get(field_name)
            if file_obj:
                # Generate a unique file name for each document
                unique_file_name = generate_unique_filename(file_obj.name)
                # Upload the file to MinIO
                if upload_file_to_minio(file_obj, unique_file_name):
                    # If upload is successful, store the unique file name in the data for serialization
                    uploaded_files[field_name] = unique_file_name
                else:
                    # If upload fails, return an error response
                    return Response({"message": f"{field_name.replace('_', ' ').capitalize()} upload failed"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Proceed with the rest of the data
        serializer = AgentProfileCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, front_side_document=request.FILES.get['front_side_document'], back_side_document=request.FILES.get['back_side_document'], created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve API View
class AgentProfileRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve an Agent Profile")
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(AgentProfile, pk=pk)
        serializer = AgentProfileRetrieveSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Update API View
class AgentProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(AgentProfile, pk=pk)
        serializer = AgentProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
