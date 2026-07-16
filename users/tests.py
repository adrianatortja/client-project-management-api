from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationAndLoginTests(APITestCase):
    def test_register_endpoint_is_not_double_nested(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'flowuser',
                'email': 'flowuser@example.com',
                'password': 'StrongPass123!',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.client.post('/api/auth/register/register/').status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_register_then_login_returns_tokens(self):
        with self.captureOnCommitCallbacks(execute=True):
            register_response = self.client.post(
                reverse('register'),
                {
                    'username': 'flowuser2',
                    'email': 'flowuser2@example.com',
                    'password': 'StrongPass123!',
                },
            )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'flowuser2', 'password': 'StrongPass123!'},
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

    def test_duplicate_email_rejected(self):
        User.objects.create_user(username='existing', email='dupe@example.com', password='pass12345')

        response = self.client.post(
            reverse('register'),
            {'username': 'newname', 'email': 'dupe@example.com', 'password': 'StrongPass123!'},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
