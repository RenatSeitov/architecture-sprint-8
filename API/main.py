from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
import jwt
import os

# Настройки
KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQ...\n-----END PUBLIC KEY-----"
ALLOWED_ROLE = "prothetic_user"

app = FastAPI()

# Настройка аутентификации через OAuth2 PKCE
auth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://keycloak.example.com/auth",
    tokenUrl="https://keycloak.example.com/token"
)

def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"], options={"verify_aud": False})
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(auth_scheme)):
    payload = decode_jwt(token)
    roles = payload.get("realm_access", {}).get("roles", [])
    if ALLOWED_ROLE not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return payload

# Фейковый отчет для API
class Report(BaseModel):
    id: int
    content: str

@app.get("/reports", response_model=list[Report])
def get_reports(user: dict = Depends(get_current_user)):
    return [
        {"id": 1, "content": "Report 1"},
        {"id": 2, "content": "Report 2"}
    ]