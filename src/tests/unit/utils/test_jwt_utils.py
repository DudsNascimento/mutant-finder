import os
import jwt
import unittest
from dataclasses import dataclass

from utils import jwt_utils

class TestJwtUtils(unittest.TestCase):

    JWT_SECRET = 'secret'
    JWT_TOKEN_EXPIRES_IN_SECONDS = '600'
    INVALID_JWT_TOKEN_EXPIRES_IN_SECONDS = '0'
    EXPIRED_JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiVGVzdCBOYW1lIiwiZXhwIjoxNjMzMzU2ODAzfQ.Nrd6jShHw0I4PbsRCtS_uJpmxWdgcNFpqW9GmezzFl8'
    INVALID_JWT_TOKEN = 'xeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiVGVzdCBOYW1lIiwiZXhwIjoxNjMzMzU2ODAzfQ.Nrd6jShHw0I4PbsRCtS_uJpmxWdgcNFpqW9GmezzFl8'

    def setUp(self):
        os.environ['JWT_SECRET'] = self.JWT_SECRET
        os.environ['JWT_TOKEN_EXPIRES_IN_SECONDS'] = self.JWT_TOKEN_EXPIRES_IN_SECONDS

    def test_generate_jwt_token(self):

        jwt_token = jwt_utils.generate_jwt_token('Test Name')
        decoded_jwt_token = jwt.decode(jwt_token, self.JWT_SECRET, algorithms=['HS256'])

        self.assertEqual(decoded_jwt_token['name'], 'Test Name')

    @dataclass
    class Request:
        headers: dict

    def test_validate_jwt_token_expired(self):

        with self.assertRaises(jwt_utils.AuthenticationError) as cm:
            jwt_utils.validate_jwt_token(
                self.Request({
                    "Authorization": "Bearer %s" % self.EXPIRED_JWT_TOKEN
                })
            )

        self.assertEqual(cm.exception.description, "Expired JWT token")

    def test_validate_jwt_token_invalid(self):

        with self.assertRaises(jwt_utils.AuthenticationError) as cm:
            jwt_utils.validate_jwt_token(
                self.Request({
                    "Authorization": "Bearer %s" % self.INVALID_JWT_TOKEN
                })
            )

        self.assertEqual(cm.exception.description, "Invalid JWT token")
