import os
import unittest
import psycopg2
from app import app
from utils import jwt_utils
from utils import database_utils

class TestApp(unittest.TestCase):

    HOSTNAME = 'test'
    PASSWORD = 'password'
    WRONG_PASSWORD = 'wrong_password'
    JWT_SECRET='secret'
    JWT_TOKEN_EXPIRES_IN_SECONDS='600'
    MAGNETO_PASSWORD='$2a$12$MnK7g3BT4zx099AbVmVz.OK5ng3YcvJdFkxGi3pHqFXBjBLjubVx.'
    DATABASE_HOST='localhost'
    DATABASE_PORT='5432'
    DATABASE_NAME='mutant_finder_test'
    DATABASE_USER='postgres'
    DATABASE_PASSWORD='postgres'
    EXPIRED_JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiVGVzdCBOYW1lIiwiZXhwIjoxNjMzMzU2ODAzfQ.Nrd6jShHw0I4PbsRCtS_uJpmxWdgcNFpqW9GmezzFl8'
    INVALID_JWT_TOKEN = 'xeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiVGVzdCBOYW1lIiwiZXhwIjoxNjMzMzU2ODAzfQ.Nrd6jShHw0I4PbsRCtS_uJpmxWdgcNFpqW9GmezzFl8'

    def setUp(self):

        os.environ['HOSTNAME'] = self.HOSTNAME
        os.environ['JWT_SECRET'] = self.JWT_SECRET
        os.environ['JWT_TOKEN_EXPIRES_IN_SECONDS'] = self.JWT_TOKEN_EXPIRES_IN_SECONDS
        os.environ['MAGNETO_PASSWORD'] = self.MAGNETO_PASSWORD
        os.environ['DATABASE_HOST'] = self.DATABASE_HOST
        os.environ['DATABASE_PORT'] = self.DATABASE_PORT
        os.environ['DATABASE_NAME'] = self.DATABASE_NAME
        os.environ['DATABASE_USER'] = self.DATABASE_USER
        os.environ['DATABASE_PASSWORD'] = self.DATABASE_PASSWORD

        #clean_database()
        self.token = jwt_utils.generate_jwt_token('Magneto')
        self.client = app.test_client()

    def test_welcome(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(b'Hello from test, welcome to Mutant DNA Finder... :)' in result.data)

    def test_login(self):
        result = self.client.post('/api/login', json = {
            'password':self.PASSWORD
        })
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.get_json()['token'] is not None)

    def test_login(self):
        result = self.client.post('/api/login', json = {
            'password':self.WRONG_PASSWORD
        })
        self.assertEqual(result.status_code, 401)
        self.assertTrue(b'Your credentials are invalid, sorry!' in result.data)

    def test_1_stats(self):
        def clean_database():
            connection = None
            try:
                connection = database_utils.connect_to_database()
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM human_dna;
                    UPDATE human_dna_statistics SET count_mutant_dna = 0, count_human_dna = 0, ratio = 0;
                    """)
                connection.commit()
                print('Database cleaned')
                cursor.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
                    print('Database connection closed.')

        clean_database()

        result = self.client.get('/api/stats', headers = {
            'Authorization':'Bearer ' + self.token
        })
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_json()['count_human_dna'], 0)
        self.assertEqual(result.get_json()['count_mutant_dna'], 0)
        self.assertEqual(result.get_json()['ratio'], 0)

    def test_2_dna_test(self):
        result = self.client.post('/api/mutant', headers = {
            'Authorization':'Bearer ' + self.token
        }, json = {
            'dna': [
                'ATCT',
                'TACA',
                'AAGA',
                'CTCA'
            ]
        })
        self.assertEqual(result.status_code, 403)
        self.assertTrue(b'Human DNA.' in result.data)

    def test_3_dna_test(self):
        result = self.client.post('/api/mutant', headers = {
            'Authorization':'Bearer ' + self.token
        }, json = {
            'dna': [
                'ATCA',
                'TAAT',
                'AAGA',
                'AAAA'
            ]
        })
        self.assertEqual(result.status_code, 200)
        self.assertTrue(b'Mutant DNA.' in result.data)

    def test_4_stats(self):
        result = self.client.get('/api/stats', headers = {
            'Authorization':'Bearer ' + self.token
        })
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_json()['count_human_dna'], 2)
        self.assertEqual(result.get_json()['count_mutant_dna'], 1)
        self.assertEqual(result.get_json()['ratio'], 0.5)

    def test_stats_expired(self):
        result = self.client.get('/api/stats', headers = {
            'Authorization':'Bearer ' + self.EXPIRED_JWT_TOKEN
        })
        self.assertEqual(result.status_code, 403)
        self.assertTrue(b'Expired JWT token' in result.data)

    def test_stats_invalid(self):
        result = self.client.get('/api/stats', headers = {
            'Authorization':'Bearer ' + self.INVALID_JWT_TOKEN
        })
        self.assertEqual(result.status_code, 403)
        self.assertTrue(b'Invalid JWT token' in result.data)
