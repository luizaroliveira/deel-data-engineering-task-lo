import os
import unittest
from unittest.mock import patch
from database.session import get_connection_arguments

class TestGetConnectionArguments(unittest.TestCase):

    @patch.dict(os.environ, {"DATABASE_USER": "testuser", "DATABASE_PASSWORD": "testpassword", "DATABASE_HOST": "testhost", "DATABASE_PORT": "5432", "DATABASE_DB": "testdb"})
    def test_get_connection_arguments_success(self):
        expected_variables = {
            "DATABASE_USER": "testuser",
            "DATABASE_PASSWORD": "testpassword",
            "DATABASE_HOST": "testhost",
            "DATABASE_PORT": "5432",
            "DATABASE_DB": "testdb"
        }
        actual_variables = get_connection_arguments()
        self.assertEqual(actual_variables, expected_variables)

    @patch.dict(os.environ, {"DATABASE_USER": "testuser", "DATABASE_PASSWORD": "testpassword", "DATABASE_HOST": "testhost", "DATABASE_PORT": "5432"})
    def test_get_connection_arguments_missing_db(self):
        with self.assertRaises(KeyError) as context:
            get_connection_arguments()
        self.assertIn("DATABASE_DB", str(context.exception))

    @patch.dict(os.environ, {"DATABASE_USER": "testuser", "DATABASE_PASSWORD": "", "DATABASE_HOST": "testhost", "DATABASE_PORT": "5432", "DATABASE_DB": "testdb"})
    def test_get_connection_arguments_empty_password(self):
        with self.assertRaises(KeyError) as context:
            get_connection_arguments()
        self.assertIn("DATABASE_PASSWORD", str(context.exception))


    @patch.dict(os.environ, {"DATABASE_USER": "testuser", "DATABASE_HOST": "testhost", "DATABASE_PORT": "5432", "DATABASE_DB": "testdb"})
    def test_get_connection_arguments_missing_multiple(self):
        with self.assertRaises(KeyError) as context:
            get_connection_arguments()
        self.assertIn("DATABASE_PASSWORD", str(context.exception))
        

    @patch.dict(os.environ, clear=True)
    def test_get_connection_arguments_missing_all(self):
        with self.assertRaises(KeyError) as context:
            get_connection_arguments()
        self.assertIn("DATABASE_USER", str(context.exception))
        self.assertIn("DATABASE_PASSWORD", str(context.exception))
        self.assertIn("DATABASE_HOST", str(context.exception))
        self.assertIn("DATABASE_PORT", str(context.exception))
        self.assertIn("DATABASE_DB", str(context.exception))



