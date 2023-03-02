from common.models import CustomBaseModel, CustomUserLogBaseModel
from users.factories.users_factories import CustomUserFactory

from .abstract_model_mixin_test_case import AbstractModelMixinTestCase


# Create your tests here.
class BaseModelTests(AbstractModelMixinTestCase):
    """
    Custom Test Case for testing CustomBaseModel essential
    functionalities
    """
    mixin = CustomBaseModel

    def test_activate_deactivate(self):
        """
        Test activation and deactivation functionality
        """
        # Create entry
        new_entry = self.model.objects.create()
        # Test deactivation method
        new_entry.deactivate()
        self.assertFalse(new_entry.is_active)
        # Test activation method
        new_entry.activate()
        self.assertTrue(new_entry.is_active)

    def test_queries(self):
        """
        Test query funcionalities
        """
        # Create entries
        entries_status = [True, False, True]
        active_entries_length = len(
            list(
                filter(
                    lambda status: status,
                    entries_status
                )
            )
        )
        inactive_entries_length = len(
            list(
                filter(
                    lambda status: not status,
                    entries_status
                )
            )
        )
        for status in entries_status:
            self.model.objects.create(is_active=status)
        # Query active entries
        active_entries = self.model.objects.query_active().all()
        self.assertEqual(len(active_entries), active_entries_length)
        # Query inactive entries
        inactive_entries = self.model.objects.query_inactive().all()
        self.assertEqual(len(inactive_entries), inactive_entries_length)


class BaseUserLogModelTests(AbstractModelMixinTestCase):
    """
    Custom TestCase for testing CustomUserLogBaseModel 
    essential functionalities
    """
    mixin = CustomUserLogBaseModel

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_creator = CustomUserFactory(is_active=True)
        cls.user_modifier = CustomUserFactory(is_active=True)
        # Create entries for query test
        for _ in range(3):
            cls.model.objects.create(
                user=cls.user_creator
            )
        for _ in range(2):
            cls.model.objects.create(
                user=cls.user_modifier
            )

    def test_create_entry(self):
        """
        Tests entry creation
        """
        # Create new entry
        new_entry = self.model.objects.create(
            user=self.user_creator
        )
        # Check created by
        self.assertEqual(new_entry.created_by.id, self.user_creator.id)
        # Check modified by
        self.assertEqual(new_entry.modified_by.id, self.user_creator.id)

    def test_activate_deactivate(self):
        """
        Tests activation and deactivation functionalities
        """
        # Create entry
        new_entry = self.model.objects.create(
            user=self.user_creator
        )
        # Test deactivate entry
        # Assures that a TypeError is raised when user is not informed
        with self.assertRaises(TypeError):
            new_entry.deactivate()
        # Check if it is inactive
        new_entry.deactivate(user=self.user_modifier)
        self.assertFalse(new_entry.is_active)
        # Check last modified by
        self.assertEqual(
            new_entry.modified_by.id,
            self.user_modifier.id
        )
        # Check if modified_by is different from created_by
        self.assertNotEqual(
            new_entry.modified_by,
            new_entry.created_by
        )
        # Test activate entry
        # Assures that a TypeError is raised when user is not informed
        with self.assertRaises(TypeError):
            new_entry.activate()
        new_entry.activate(user=self.user_creator)
        # Check if it is active
        self.assertTrue(new_entry.is_active)
        # Check if modified_by is changed
        self.assertEqual(
            new_entry.modified_by.id,
            self.user_creator.id
        )

    def test_query_by_user_creator(self):
        """
        Tests query by user creator
        """
        # Assures that an error is raised when no user is informed
        with self.assertRaises(TypeError):
            self.model.objects.query_by_user_creator()
        query_result = self.model.objects.query_by_user_creator(
            user=self.user_creator
        ).all()
        self.assertEqual(len(query_result), 3)
        self.assertNotEqual(len(query_result), len(self.model.objects.all()))
