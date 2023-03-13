from datetime import datetime, date

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
        cls.user_3 = CustomUserFactory(
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
        cls.tasks['task_10'] = TaskFactory(
            name="Task 10",
            project=cls.projects['project_7'],
            is_active=True,
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        cls.tasks['task_11'] = TaskFactory(
            name="Task 11",
            project=cls.projects['project_7'],
            is_active=True,
            created_by=cls.user_2,
            modified_by=cls.user_2
        )
        Cycles.objects.create(
            user=cls.user_2,
            is_active=True,
            task=cls.tasks['task_10'],
            dt_start=datetime(2023, 2, 27, 1, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 27, 2, tzinfo=pytz.UTC)
        )
        Cycles.objects.create(
            user=cls.user_2,
            is_active=True,
            task=cls.tasks['task_10'],
            dt_start=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC)
        )
        Cycles.objects.create(
            user=cls.user_2,
            is_active=True,
            task=cls.tasks['task_11'],
            dt_start=datetime(2023, 3, 1, 4, tzinfo=pytz.UTC)
        )
        cls.expected_project_ranking = ['Project 2', 'Project 4', 'Project 6', 'Project 5', 'Project 3']
        cls.expected_task_ranking = ['Task 9', 'Task 6', 'Task 5', 'Task 4', 'Task 8']
        # Last month and week test
        project_feb = ProjectFactory(
            name="Project Feb 001",
            is_active=True,
            created_by=cls.user_3,
            modified_by=cls.user_3,
            created_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC)
        )
        task_feb_001 = TaskFactory(
            name="Task Feb 001",
            project=project_feb,
            is_active=True,
            created_by=cls.user_3,
            modified_by=cls.user_3,
            created_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC)
        )
        Cycles.objects.create(
            user=cls.user_3,
            is_active=True,
            task=task_feb_001,
            created_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC),
            dt_start=datetime(2023, 2, 22, 1, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 22, 6, tzinfo=pytz.UTC)
        )
        project_mar = ProjectFactory(
            name="Project Mar 001",
            is_active=True,
            created_by=cls.user_3,
            modified_by=cls.user_3,
            created_on=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC)
        )
        task_mar_001 = TaskFactory(
            name="Task Mar 001",
            project=project_mar,
            is_active=True,
            created_by=cls.user_3,
            modified_by=cls.user_3,
            created_on=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 3, 1, 1, 1, tzinfo=pytz.UTC)
        )
        Cycles.objects.create(
            user=cls.user_3,
            is_active=True,
            task=task_mar_001,
            created_on=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            dt_start=datetime(2023, 3, 1, 1, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 3, 1, 4, tzinfo=pytz.UTC)
        )
        Cycles.objects.create(
            user=cls.user_3,
            is_active=True,
            task=task_mar_001,
            created_on=datetime(2022, 3, 1, 1, tzinfo=pytz.UTC),
            modified_on=datetime(2022, 3, 1, 1, tzinfo=pytz.UTC),
            dt_start=datetime(2022, 3, 1, 1, tzinfo=pytz.UTC),
            dt_end=datetime(2022, 3, 1, 4, tzinfo=pytz.UTC)
        )

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

    def test_open_tasks(self):
        self.client.force_authenticate(user=self.user_2)
        url = reverse('open_tasks')
        response = self.client.get(url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertEqual(
            set(['Task 10', 'Task 11']),
            set([_['name'] for _ in response.data])
        )

    def test_latest_tasks(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse('latest_tasks')
        response = self.client.get(url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertEqual(
            ['Task 9', 'Task 8', 'Task 6', 'Task 5', 'Task 4'],
            [tk['name'] for tk in response.data]
        )

    def test_total_time(self):
        self.client.force_authenticate(user=self.user_3)
        date_target = date(2023, 3, 3).strftime('%Y-%m-%d')
        url = reverse(
            'total_time',
        )
        response = self.client.get(
            url,
            {'date_target': date_target}
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        #TODO assert week current value and last value
        # Current value
        self.assertEqual(
            10800,
            response.data['week']['additional_info']['current_value']
        )
        # Last value
        self.assertEqual(
            18000,
            response.data['week']['additional_info']['last_value']
        )
        #TODO assert month current value and last value
        self.assertEqual(
            10800,
            response.data['month']['additional_info']['current_value']
        )
        # Last value
        self.assertEqual(
            18000,
            response.data['month']['additional_info']['last_value']
        )
        #TODO assert year current value and last value
        self.assertEqual(
            28800,
            response.data['year']['additional_info']['current_value']
        )
        self.assertEqual(
            28800,
            response.data['year']['additional_info']['current_value']
        )

    def test_total_time_first_year_week(self):
        self.client.force_authenticate(user=self.user_3)
        date_target = date(2023, 1, 1).strftime('%Y-%m-%d')
        url = reverse(
            'total_time'
        )
        response = self.client.get(
            url,
            {'date_target': date_target}
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
