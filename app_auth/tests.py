from django.test import TestCase
# app_auth/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from app_auth.models.user import CustomUser  # Adjust this import if necessary
from django.contrib.auth.models import Group

# Create your tests here.
class CustomTokenTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User'
        )
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)

    def test_obtain_token(self):
        url = reverse('custom_token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('groups', response.data)
        self.assertIn('Test Group', response.data['groups'])

    def test_obtain_token_invalid_credentials(self):
        url = reverse('custom_token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_refresh_token(self):
        # First obtain a valid refresh token
        url = reverse('custom_token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        # Use the refresh token to get a new access token
        refresh_url = reverse('custom_token_refresh')
        refresh_data = {
            'refresh': refresh_token
        }
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_refresh_token_invalid(self):
        refresh_url = reverse('custom_token_refresh')
        refresh_data = {
            'refresh': 'invalid-refresh-token'
        }
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', refresh_response.data)


