"""
Filename: test_middleware.py
Author: George Deamont <deamontg@gmail.com>
Description: Database tests.
"""

from falcon import testing

from app.database import Database


class DatabaseTestCase(testing.TestCase):
    """
    """

    def setUp(self):
        """
        TODO: Create test database and perform alembic migrations.
        """
        pass


    def tearDown(self):
        """
        TODO: Delete test database
        """
        pass