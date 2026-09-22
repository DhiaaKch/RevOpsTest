import jwt

# BAD: secret committed directly to source code
SECRET_KEY = "super_secret_key_12345"

def create_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
