from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from tasktime.factories.tasktime_factories import ProjectFactory, TaskFactory
from tasktime.models import Cycles
from users.factories.users_factories import CustomUserFactory


class DurationTests(TestCase):
    """
    TestCase to test if the durations
    are being correctly evaluated
    """
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUserFactory(
            is_active=True
        )
        cls.project = ProjectFactory(
            created_by=cls.test_user,
            modified_by=cls.test_user
        )
        cls.task_1 = TaskFactory(
            project=cls.project,
            created_by=cls.test_user,
            modified_by=cls.test_user
        )
        cls.task_2 = TaskFactory(
            project=cls.project,
            created_by=cls.test_user,
            modified_by=cls.test_user
        )
        cls.cycle_1 = Cycles.objects.create(
            task=cls.task_1,
            dt_start=datetime(2023, 2, 2, 7, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 8, tzinfo=pytz.UTC),
            user=cls.test_user,
        )
        cls.cycle_2 = Cycles.objects.create(
            task=cls.task_1,
            dt_start=datetime(2023, 2, 2, 6, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 6, 30, tzinfo=pytz.UTC),
            user=cls.test_user,
        )
        cls.cycle_3 = Cycles.objects.create(
            task=cls.task_1,
            dt_start=datetime(2023, 2, 2, 8, 30, tzinfo=pytz.UTC),
            user=cls.test_user,
        )
        cls.cycle_4 = Cycles.objects.create(
            task=cls.task_2,
            dt_start=datetime(2023, 2, 2, 6, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 6, 30, tzinfo=pytz.UTC),
            user=cls.test_user,
        )
        cls.cycle_5 = Cycles.objects.create(
            task=cls.task_2,
            dt_start=datetime(2023, 2, 2, 7, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 8, 30, tzinfo=pytz.UTC),
            user=cls.test_user,
        )
        cls.wrong_cycle = Cycles.objects.create(
            task=cls.task_2,
            dt_start=datetime(2023, 2, 2, 10, tzinfo=pytz.UTC),
            dt_end=datetime(2023, 2, 2, 9, tzinfo=pytz.UTC),
            user=cls.test_user,
        )

    def test_cycles_duration(self):
        self.assertEqual(
            self.cycle_1.duration,
            3600
        )
        self.assertEqual(
            self.cycle_1.parsed_duration,
            "01:00:00"
        )
        with self.assertRaises(ValueError):
            self.cycle_3.duration
        with self.assertRaises(ValueError):
            self.wrong_cycle.duration

    def test_tasks_duration(self):
        self.assertEqual(
            self.task_1.duration,
            5400
        )
        self.assertEqual(
            self.task_1.parsed_duration,
            "01:30:00"
        )

    def test_project_duration(self):
        self.assertEqual(
            self.project.duration,
            12600
        )
        self.assertEqual(
            self.project.parsed_duration,
            "03:30:00"
        )
