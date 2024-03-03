from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import re

auth_router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)
# Define a Pydantic model for the user credentials
class UserCredentials(BaseModel):
    email: str
    password: str

# Secret key for JWT token encoding/decoding
SECRET_KEY = "your-secret-key"

# Generate a JWT token based on user credentials
def generate_token(credentials: UserCredentials) -> str:
    # Here, you can add your own logic to authenticate the user based on the email and password.
    # For simplicity, let's assume the user is authenticated if the email is "test@example.com" and the password is "password".
    if is_valid_email(credentials.email):
        # Create the payload for the token
        payload = {
            "sub": credentials.email,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        # Encode the token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

# Endpoint to generate a JWT token
@auth_router.post("/token")
def get_token(credentials: UserCredentials):
    token = generate_token(credentials)
    return {"token": token}

# Validation for email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Dependency for JWT authentication
def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email:
            return email
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")