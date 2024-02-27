# jwt_handler.py
import jwt
import datetime
import os
from jwt import exceptions
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_secret_key')

def generate_token(user_id, name, nickname):
    payload = {
        "sub": user_id,  # Subject, typically the user ID
        "name": name,
        "nickname": nickname,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")




def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # or True, based on your implementation
    except exceptions.ExpiredSignatureError:
        # Token has expired
        print("Token expired")
        return False  # or raise an exception
    except exceptions.DecodeError:
        # Token is invalid
        print("Token invalid")
        return False  # or raise an exception
