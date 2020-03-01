from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""
    CREATE_USER_URL = reverse('user:create')
    TOKEN_URL = reverse('user:token')

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'user_test@email.com',
            'password': 'test_password_1234',
            'name': 'Full Name',
        }

        response = self.client.post(self.CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'user_test@email.com',
            'password': 'test_password_1234',
            'name': 'Full Name'
        }
        self.create_user(**payload)

        response = self.client.post(self.CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 charecters"""
        payload = {
            'email': 'user_test@email.com',
            'password': '1234567',
            'name': 'Full Name'
        }

        response = self.client.post(self.CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'user@email.com', 'password': 'test_user_pass_1234'}
        self.create_user(**payload)
        response = self.client.post(self.TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that token is not created if invalid credentials are given"""
        self.create_user(email='user@email.com', password='user_password_1234')
        payload = {'email': 'user@email.com', 'password': 'wrong_pass'}

        response = self.client.post(self.TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exists"""
        payload = {'email': 'non_exist_user@email.com', 'password': 'non_user_password_test_1234'}
        response = self.client.post(self.TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password required"""
        response = self.client.post(self.TOKEN_URL, {'email': 'user@email.com', 'password': ''})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_user(self, **params):
        return get_user_model().objects.create_user(**params)
