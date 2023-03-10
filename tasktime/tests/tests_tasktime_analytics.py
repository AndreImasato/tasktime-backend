from datetime import datetime

import pytz
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasktime.factories.tasktime_factories import ProjectFactory, TaskFactory
from tasktime.models import Cycles
from users.factories.users_factories import CustomUserFactory


class AnalyticsTests(APITestCase):
    """
    TestCase for testing analytics
    related features (endpoints, functionalities)
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = CustomUserFactory(
            is_active=True
        )
        cls.user_2 = CustomUserFactory(
            is_active=True
        )
        cls.projects = {}
        cls.tasks = {}
        cls.cycles = {}
        for i in range(1, 7):
            cls.projects[f'project_{i}'] = ProjectFactory(
                name=f"Project {i}",
                is_active=True,
                created_by=cls.user_1,
                modified_by=cls.user_1
            )
            cls.tasks[f'task_{i}'] = TaskFactory(
                name=f"Task {i}",
                project=cls.projects[f'project_{i}'],
                is_active=True,
                created_by=cls.user_1,
                modified_by=cls.user_1
            )
            cls.cycles[f'cycle_{i}'] = Cycles.objects.create(
                user=cls.user_1,
                is_active=True,
                task=cls.tasks[f'task_{i}'],
                dt_start=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
                dt_end=datetime(2023, 3, 1, i + 1, tzinfo=pytz.UTC)
            )
        cls.projects['project_7'] = ProjectFactory(
            name="Project 7",
            is_active=True,
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        cls.tasks['task_7'] = TaskFactory(
            name="Task 7",
            project=cls.projects['project_7'],
            is_active=True,
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        cls.cycles['cycle_7'] = Cycles.objects.create(
            user=cls.user_2,
            is_active=True,
            task=cls.tasks['task_7'],
            dt_start=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 3, 1, 23, tzinfo=pytz.UTC)
        )
        cls.tasks['task_8'] = TaskFactory(
            name="Task 8",
            project=cls.projects['project_4'],
            is_active=True,
            created_by=cls.user_1,
            modified_by=cls.user_1
        )
        cls.cycles['cycle_8'] = Cycles.objects.create(
            user=cls.user_1,
            is_active=True,
            task=cls.tasks['task_8'],
            dt_start=datetime(2023, 3, 1, 5, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 3, 1, 9, tzinfo=pytz.UTC)
        )
        cls.tasks['task_9'] = TaskFactory(
            name="Task 9",
            project=cls.projects['project_2'],
            is_active=True,
            created_by=cls.user_1,
            modified_by=cls.user_1
        )
        cls.cycles['cycle_9'] = Cycles.objects.create(
            user=cls.user_1,
            is_active=True,
            task=cls.tasks['task_9'],
            dt_start=datetime(2023, 3, 1, 3, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 3, 1, 10, tzinfo=pytz.UTC)
        )
        cls.expected_project_ranking = ['Project 2', 'Project 4', 'Project 6', 'Project 5', 'Project 3']
        cls.expected_task_ranking = ['Task 9', 'Task 6', 'Task 5', 'Task 4', 'Task 8']

    def test_ranking(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse('duration_ranking')
        response = self.client.get(url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertEqual(
            tuple(self.expected_project_ranking),
            tuple(response.data['projects']['labels'])
        )
        self.assertEqual(
            tuple(self.expected_task_ranking),
            tuple(response.data['tasks']['labels'])
        )
