import os
from copy import copy
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories.users_factories import CustomUserFactory

# Create your tests here.
User = get_user_model()


class UsersManagersTests(TestCase):
    """
    TestCase for testing creating users with
    managers method

    Testing contexts:
    1. Create common user
    2. Create super user
    """

    def test_create_user(self):
        """
        Test method to create a common user
        """
        user = User.objects.create_user(
            email="normal@user.com",
            username="common",
            password="foo"
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.username, "common")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.public_id)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(TypeError):
            User.objects.create_user(email="", username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", username="", password="foo")

    def test_create_superuser(self):
        """
        Test method to create a super user
        """
        admin_user = User.objects.create_superuser(
            email="super@user.com",
            username="admin",
            password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNotNone(admin_user.public_id)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com",
                username="admin",
                password="foo",
                is_superuser=False
            )


class SuperUserCommandTests(TestCase):
    """
    TestCase for testing the create_super_user command
    Testing contexts:
    1. With user input
    2. Without user input
    """
    def tearDown(self) -> None:
        """
        In case any of these environment variables
        are set, unset them
        """
        os.unsetenv('DJANGO_SUPERUSER_USERNAME')
        os.unsetenv('DJANGO_SUPERUSER_EMAIL')
        os.unsetenv('DJANGO_SUPERUSER_PASSWORD')

    @tag('exclude_git_commit')
    def test_command_input(self):
        """
        Test method for the command execution
        with user inputs.

        The inputs are mocked by using the default
        unittest mock utilites
        """
        # Mock for username input
        input_mock_user = mock.Mock(return_value='test_input')
        # Mock for user email input
        input_mock_email = mock.Mock(return_value="test.input@test.com")
        # Mock for user password input
        input_mock_password = mock.Mock(return_value="pTaesssTwuosrEdr@")
        # Mock for user password confirmation input
        input_mock_password_confirm = mock.Mock(
            return_value="pTaesssTwuosrEdr@"
        )
        # Combine the mocked inputs for the "get_input_data" method
        input_mock = mock.Mock(side_effect=[
            input_mock_user.return_value,
            input_mock_email.return_value,
        ])
        # Combine the mocked inputs for the "getpass" method
        input_mock_sensitive = mock.Mock(side_effect=[
            input_mock_password.return_value,
            input_mock_password_confirm.return_value
        ])
        # Mock for bypassing "weak" password input call
        input_mock_password_bypass = mock.Mock(return_value="y")
        # Variable to store command output
        out = StringIO()
        # Defining stdout argument for command execution
        kwargs = {'stdout': out}
        # Patching all input-like methods
        with mock.patch('users.management.commands.custom_create_superuser.'
                        'Command.get_input_data', input_mock), \
                mock.patch('getpass.getpass', input_mock_sensitive), \
                mock.patch('builtins.input', input_mock_password_bypass):
            # Calling command
            call_command(
                'custom_create_superuser',
                **kwargs
            )
        # Asserting that the command output contains the desired message
        self.assertIn("Superuser created successfully.", out.getvalue())
        # Asserting that the user was created correctly
        super_user = User.objects.filter(email='test.input@test.com')
        self.assertTrue(super_user.exists)
        self.assertTrue(super_user.first().is_superuser)
        self.assertIsNotNone(super_user.first().public_id)

    def test_command_no_input(self):
        """
        Test method for the command execution without
        user inputs.

        In this case a few environment variables must be set
        """
        # Setting up the required environment variables
        # for no-input command execution
        os.environ['DJANGO_SUPERUSER_USERNAME'] = 'test'
        os.environ['DJANGO_SUPERUSER_EMAIL'] = 'test@test.com'
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'password'
        # Variable to store command ouput
        out = StringIO()
        # Argument to call the command without user input
        args = [
            '--no-input',
        ]
        # Defining stdout argument for command execution
        kwargs = {'stdout': out}

        call_command(
            'custom_create_superuser',
            *args,
            **kwargs
        )
        # Asserting that the command output contains the desired message
        self.assertIn('Superuser created successfully.', out.getvalue())
        # Asserting that the user was correctly created
        super_user = User.objects.filter(email='test@test.com')
        self.assertTrue(super_user.exists)
        self.assertTrue(super_user.first().is_superuser)
        self.assertIsNotNone(super_user.first().public_id)


class UsersActivationTests(TestCase):
    """
    TestCase for testing activate and de-activate
    methods functionality
    """
    def test_activate_deactivate(self):
        # To instantiate the CustomUser model
        user = User.objects.create_user(
            email="normal@user.com",
            username="common",
            password="foo"
        )
        # Deactivate user
        user.deactivate()
        self.assertFalse(user.is_active)
        # Reactivate user
        user.activate()
        self.assertTrue(user.is_active)


class UsersQueryByStatusTests(TestCase):
    """
    TestCase for testing querying users
    by theirs status
    """
    def test_query_by_status(self):
        # Create 4 users
        users_status = [True, True, True, False]
        users_active_length = len(
            list(
                filter(
                    lambda status: status,
                    users_status
                )
            )
        )
        users_inactive_length = len(
            list(
                filter(
                    lambda status: not status,
                    users_status
                )
            )
        )
        for stt in users_status:
            CustomUserFactory(is_active=stt)
        # Query active users
        active_users = User.objects.query_active().all()
        self.assertEqual(len(active_users), users_active_length)
        # Query inactive users
        inactive_users = User.objects.query_inactive().all()
        self.assertEqual(len(inactive_users), users_inactive_length)


class UsersEndpointTest(APITestCase):
    """
    TestCase for testing users related endpoints
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_admin = User.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="admin"
        )
        cls.base_data = {
            "email": "user@test.com",
            "password": "password",
            "password_confirmation": "password",
            "username": "user"
        }
        cls.base_url = reverse('users-list')

    def setUp(self):
        self.test_user = User.objects.create_user(
            email="test_user@test.com",
            username="test_user",
            password="password"
        )
        self.detail_url = reverse(
            'users-detail',
            kwargs={"public_id": self.test_user.public_id}
        )

    def test_without_authentication(self):
        """
        Test without authenticate
        Checks for 401 return
        """
        response = self.client.post(
            self.base_url,
            data=self.base_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        """
        Test for user creation endpoint
        """
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(
            self.base_url,
            data=self.base_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_password(self):
        """
        Test user creation without matching
        password confirmation
        """
        self.client.force_authenticate(user=self.user_admin)
        test_data = copy(self.base_data)
        test_data['password_confirmation'] = "wrongpassword"
        response = self.client.post(
            self.base_url,
            data=test_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user(self):
        """
        Test to retrieve a user
        """
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.test_user.email)

    def test_patch_user(self):
        """
        Test for patching user information
        """
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.patch(
            self.detail_url,
            data={'first_name': 'Test', 'last_name': 'User'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_user(self):
        """
        Test for deleting a user
        """
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
