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
            is_active=True,
            created_by=cls.user_1,
            modified_by=cls.user_1
        )
        cls.project_2 = ProjectFactory(
            is_active=True,
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        cls.project_3 = ProjectFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=False
        )
        cls.project_4 = ProjectFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=True
        )
        cls.task_1 = TaskFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=True,
            project=cls.project_1
        )
        cls.task_2 = TaskFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=False,
            project=cls.project_1
        )
        cls.task_3 = TaskFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=True,
            project=cls.project_2
        )
        cls.task_4 = TaskFactory(
            created_by=cls.user_1,
            modified_by=cls.user_1,
            is_active=True,
            project=cls.project_4
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
            2
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
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertDictContainsSubset(
            {'name': 'Test Project'},
            response.data
        )

    def test_project_patch(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'projects-detail',
            kwargs={
                'public_id': self.project_1.public_id
            }
        )
        response = self.client.patch(
            url,
            data={
                'name': 'Patched Project'
            },
            format='json'
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertDictContainsSubset(
            {'name': 'Patched Project'},
            response.data
        )

    def test_project_patch_from_other_user(self):
        self.client.force_authenticate(
            user=self.user_2
        )
        url = reverse(
            'projects-detail',
            kwargs={
                'public_id': self.project_1.public_id
            }
        )
        response = self.client.patch(
            url,
            data={
                'name': "Other user project"
            },
            format="json"
        )
        self.assertEqual(
            status.HTTP_404_NOT_FOUND,
            response.status_code
        )

    def test_project_delete(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'projects-detail',
            kwargs={
                'public_id': self.project_1.public_id
            },
        )
        response = self.client.delete(
            url
        )
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code
        )

    def test_task_create(self):
        """
        Test for task creation
        """
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse('tasks-list')
        response = self.client.post(
            url,
            data={
                'name': "Task Test",
                'project': self.project_1.id
            },
            format="json"
        )
        self.assertEqual(
            status.HTTP_201_CREATED,
            response.status_code
        )
        self.assertDictContainsSubset(
            {'name': "Task Test"},
            response.data
        )

    def test_task_patch(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'tasks-detail',
            kwargs={
                'public_id': self.task_1.public_id
            }
        )
        response = self.client.patch(
            url,
            data={
                'name': 'Patched Task'
            },
            format="json"
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertDictContainsSubset(
            {'name': 'Patched Task'},
            response.data
        )

    def test_task_delete(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'tasks-detail',
            kwargs={
                'public_id': self.task_1.public_id
            }
        )
        response = self.client.delete(
            url,
        )
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code
        )
