import os
import unittest 
from unittest.mock import patch

from utils import database_utils

class TestDatabaseUtils(unittest.TestCase):

    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DATABASE_NAME = 'mutant_finder'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'postgres'

    def setUp(self):
        os.environ['DATABASE_HOST'] = self.DATABASE_HOST
        os.environ['DATABASE_PORT'] = self.DATABASE_PORT
        os.environ['DATABASE_NAME'] = self.DATABASE_NAME
        os.environ['DATABASE_USER'] = self.DATABASE_USER
        os.environ['DATABASE_PASSWORD'] = self.DATABASE_PASSWORD

    @patch('psycopg2.connect')
    def test_connect_to_database(self, psycopg2_connect_call):
        psycopg2_connect_call.return_value = None
        result = database_utils.connect_to_database()
        self.assertEqual(psycopg2_connect_call.call_count, 1)
