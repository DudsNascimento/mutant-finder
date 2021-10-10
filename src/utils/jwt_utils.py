import os
import jwt
import datetime

class AuthenticationError(Exception):
    def __init__(self, description, code = 403):
        self.description = description
        self.code = code

def generate_jwt_token(name):
    return jwt.encode({
            "name": name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(0, int(os.environ['JWT_TOKEN_EXPIRES_IN_SECONDS'])),
        }, os.environ['JWT_SECRET'], algorithm="HS256")

def validate_jwt_token(request):
    jwt_token = request.headers['Authorization'].replace('Bearer ', '')
    try:
        jwt.decode(jwt_token, os.environ['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Expired JWT token")
    except Exception:
        raise AuthenticationError("Invalid JWT token")