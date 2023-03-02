from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasktime.factories.tasktime_factories import ProjectFactory, TaskFactory
from tasktime.models import Cycles
from users.factories.users_factories import CustomUserFactory


class TasktimeEndpointsTest(APITestCase):
    """
    TestCase for testing tasktime
    related endpoints
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = CustomUserFactory(
            is_active=True
        )
        cls.user_2 = CustomUserFactory(
            is_active=True
        )
        cls.project_1 = ProjectFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1
        )
        cls.project_2 = ProjectFactory(
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        cls.project_3 = ProjectFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=False
        )

    def test_without_authentication(self):
        """
        Test without authenticate
        """
        url = reverse('projects-list')
        response = self.client.get(
            url
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        #TODO do the same for tasks
        #TODO do the same for cycles

    def test_projects_list(self):
        """
        Test projects listing
        """
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse('projects-list')
        response = self.client.get(
            url
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            1
        )

    def test_projects_create(self):
        """
        Test project creation
        """
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse('projects-list')
        response = self.client.post(
            url,
            data={
                "name": "Test Project"
            },
            format="json"
        )
        print(response.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertDictContainsSubset(
            {'name': 'Test Project'},
            response.data
        )
