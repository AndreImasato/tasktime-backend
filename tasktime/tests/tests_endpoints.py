from datetime import datetime

import pytz
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
        cls.cycle_1 = Cycles.objects.create(
            user=cls.user_1,
            is_active=True,
            task=cls.task_1,
            dt_start=datetime(2023, 2, 2, 6, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 7, 30, tzinfo=pytz.UTC)
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

    def test_cycle_create(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse('cycles-list')
        correct_data = {
            'task': self.task_1.id,
            'dt_start': datetime(2023, 2, 2, 10, tzinfo=pytz.UTC)
        }
        wrong_data = {
            'task': self.task_3.id,
            'dt_start': datetime(2023, 2, 2, 9, tzinfo=pytz.UTC),
            'dt_end': datetime(2023, 2, 2, 8, tzinfo=pytz.UTC)
        }
        response_correct = self.client.post(
            url,
            data=correct_data,
            format="json"
        )
        self.assertEqual(
            status.HTTP_201_CREATED,
            response_correct.status_code
        )
        response_wrong = self.client.post(
            url,
            data=wrong_data,
            format="json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response_wrong.status_code
        )

    def test_cycle_patch(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'cycles-detail',
            kwargs={
                'public_id': self.cycle_1.public_id
            }
        )
        response_correct = self.client.patch(
            url,
            format="json",
            data={
                'dt_end': datetime(2023, 2, 3, 7, 30, tzinfo=pytz.UTC)
            }
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response_correct.status_code
        )
        response_error = self.client.patch(
            url,
            format="json",
            data={
                'dt_end': datetime(2023, 2, 1, 7, 30, tzinfo=pytz.UTC)
            }
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response_error.status_code
        )

    def test_cycle_delete(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'cycles-detail',
            kwargs={
                'public_id': self.cycle_1.public_id
            }
        )
        response = self.client.delete(
            url
        )
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code
        )

    def test_create_cycle_within_another_interval(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        url = reverse(
            'cycles-list'
        )
        response = self.client.post(
            url,
            format="json",
            data={
                'dt_start': datetime(2023, 2, 2, 7, tzinfo=pytz.UTC),
                'is_active': True,
                'task': self.task_1.id,
            }
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code
        )
        self.assertTrue(
            'message' in response.data
        )
        self.assertTrue(
            'início' in response.data['message']
        )
        response = self.client.post(
            url,
            format="json",
            data={
                'dt_start': datetime(2023, 2, 2, 5, tzinfo=pytz.UTC),
                'dt_end': datetime(2023, 2, 2, 7, tzinfo=pytz.UTC),
                'is_active': True,
                'task': self.task_1.id,
            }
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code
        )
        self.assertTrue(
            'message' in response.data
        )
        self.assertTrue(
            'término' in response.data['message']
        )

    def test_patch_cycle_within_another_interval(self):
        self.client.force_authenticate(
            user=self.user_1
        )
        cycle_2 = Cycles.objects.create(
            user=self.user_1,
            is_active=True,
            task=self.task_1,
            dt_start=datetime(2023, 2, 2, 8, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 8, 30, tzinfo=pytz.UTC)
        )
        cycle_3 = Cycles.objects.create(
            user=self.user_1,
            is_active=True,
            task=self.task_1,
            dt_start=datetime(2023, 2, 2, 5, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 5, 30, tzinfo=pytz.UTC)
        )
        # Test patching dt_start within another interval
        url = reverse(
            'cycles-detail',
            kwargs={
                'public_id': cycle_2.public_id
            }
        )
        response = self.client.patch(
            url,
            format="json",
            data={
                'dt_start': datetime(2023, 2, 2, 6, 30, tzinfo=pytz.UTC)
            }
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code
        )
        self.assertTrue(
            'message' in response.data
        )
        self.assertTrue(
            'início' in response.data['message']
        )
        # Test patching dt_end within another interval
        url = reverse(
            'cycles-detail',
            kwargs={
                'public_id': cycle_3.public_id
            }
        )
        response = self.client.patch(
            url,
            format="json",
            data={
                'dt_end': datetime(2023, 2, 2, 7, tzinfo=pytz.UTC)
            }
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code
        )
        self.assertTrue(
            'message' in response.data
        )
        self.assertTrue(
            'término' in response.data['message']
        )
