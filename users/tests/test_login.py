from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import UserAccessLogs

User = get_user_model()


class LoginTests(APITestCase):
    def setUp(self):
        self.password = "testpassword"
        self.wrong_password = "wrongpassword"
        self.test_user = User.objects.create_user(
            email="test@user.com",
            username="testuser",
            password=self.password
        )

    def test_login(self):
        """
        TestCase for testing login endpoint
        It will be tested whether a valid token is returned
        or not
        """
        url = reverse('user_login')
        data = {
            "email": self.test_user.email,
            "password": self.password
        }
        response = self.client.post(
            url,
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data.keys())
        self.assertIn('access', response.data.keys())

    def test_wrong_login(self):
        """
        TestCase for testing login endpoint
        It will be tested whether a 400 status code is returned
        for wrong credentials or not
        """
        url = reverse('user_login')
        data = {
            "email": self.test_user.email,
            "password": self.wrong_password
        }
        response = self.client.post(
            url,
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_log(self):
        """
        TestCase for testing user access log
        It will be tested whether the user access is
        being registered
        """
        initial_access_count = UserAccessLogs.objects.all().count()
        url = reverse('user_login')
        data = {
            "email": self.test_user.email,
            "password": self.password
        }
        self.client.post(
            url,
            data,
            format="json"
        )
        post_email_login_access_count = UserAccessLogs.objects.all()
        self.assertEqual(
            post_email_login_access_count.count(),
            initial_access_count + 1
        )
