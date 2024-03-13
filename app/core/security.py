from typing import Optional, List
from pydantic import BaseModel, EmailStr
from firebase_admin import auth
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

class FirebaseIdentities(BaseModel):
    microsoft_com: Optional[List[str]] = []
    email: Optional[List[EmailStr]] = []

class FirebaseDetails(BaseModel):
    identities: Optional[FirebaseIdentities]
    sign_in_provider: Optional[str]

class DecodedToken(BaseModel):
    name: Optional[str] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
    auth_time: Optional[int] = None
    user_id: Optional[str] = None
    sub: Optional[str] = None
    iat: Optional[int] = None
    exp: Optional[int] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    firebase: Optional[FirebaseDetails] = None
    uid: Optional[str] = None

async def get_user(request: Request, token: HTTPAuthorizationCredentials = Depends(security)) -> DecodedToken:
    try:
        jwt = token.credentials
        decoded_token = auth.verify_id_token(jwt)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    return DecodedToken(**decoded_token)