from django.db import connection
from django.db.models.base import ModelBase
from django.db.utils import OperationalError
from django.test import TestCase


class AbstractModelMixinTestCase(TestCase):
    """
    Base class for tests of model mixin/abstract models.
    To use, subclass and specify the mixin class variable.
    A model using the mixin will be made available in self.model.
    """
    @classmethod
    def setUpClass(cls):
        # Create a dummy model which extends the mixin.
        # A RuntimeWarning will occur if the model is
        # registered twice.
        if not hasattr(cls, 'model'):
            cls.model = ModelBase(
                '__TestModel__' +
                cls.mixin.__name__, (cls.mixin, ),
                {'__module__': cls.mixin.__module__}
            )

        # Create the schema for the test model. If the table
        # already exists, will pass
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls.model)
            super(AbstractModelMixinTestCase, cls).setUpClass()
        except OperationalError:
            pass

    @classmethod
    def tearDownClass(cls):
        # Delete the schema for the test model. If there's
        # no table, will pass
        super(AbstractModelMixinTestCase, cls).tearDownClass()
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(cls.model)
        except OperationalError:
            pass
