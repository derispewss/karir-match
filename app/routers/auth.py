"""Authentication router – Phase 6‑03.

Provides:
- **POST /auth/register** – creates a user and returns a JWT.
- **POST /auth/login** – verifies credentials, applies a simple per‑IP rate‑limit, and returns a JWT.
- **GET /auth/me** – protected endpoint that returns the current user info (demo). 
- **POST /auth/logout** – client‑side logout (deletes cookie).

JWT handling is delegated to :pymod:`app.utils.jwt`. In production you would store the secret in env vars, use HTTPS‑only cookies, CSRF tokens, and a more robust rate‑limit (Redis, etc.).
"""

import time
from typing import Optional
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import SessionLocal
from .. import crud, models
from ..utils.jwt import create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------------------------------------------
# DB dependency
# -------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------------------
# Pydantic schemas
# -------------------------------------------------------------------
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# -------------------------------------------------------------------
# Helper utilities
# -------------------------------------------------------------------
def _hash(pw: str) -> str:
    return pwd_ctx.hash(pw)

def _verify(pw: str, h: str) -> bool:
    return pwd_ctx.verify(pw, h)

# Simple in‑memory rate‑limit for login (IP → timestamps)
_LOGIN_ATTEMPTS: dict[str, list[float]] = {}
_LOGIN_LIMIT = 5  # max attempts per minute per IP

def check_login_rate_limit(request: Request):
    ip = request.client.host
    now = time.time()
    attempts = _LOGIN_ATTEMPTS.get(ip, [])
    # keep only attempts in the last 60 seconds
    attempts = [t for t in attempts if now - t < 60]
    if len(attempts) >= _LOGIN_LIMIT:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try later.")
    attempts.append(now)
    _LOGIN_ATTEMPTS[ip] = attempts

# -------------------------------------------------------------------
# Dependency to retrieve the current user from a JWT
# -------------------------------------------------------------------
def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1]
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# -------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------
@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = _hash(payload.password)
    user = crud.create_user(
        db,
        email=payload.email,
        hashed_password=hashed,
        full_name=payload.full_name,
    )
    token = create_access_token(user_id=user.id)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(payload: RegisterIn, request: Request, db: Session = Depends(get_db)):
    # Apply simple rate‑limit per IP
    check_login_rate_limit(request)
    user = crud.get_user_by_email(db, payload.email)
    if not user or not _verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_id=user.id)
    return TokenOut(access_token=token)

@router.get("/me", response_model=dict)
def read_current_user(current: models.User = Depends(get_current_user)):
    """Return minimal info about the authenticated user (demo purpose)."""
    return {
        "user_id": current.id,
        "email": current.email,
        "full_name": current.full_name,
        "is_admin": current.is_admin,
    }

@router.post("/logout")
def logout(response: Response):
    """Stateless logout – delete bearer token cookie if client stores it.
    In a JWT‑only flow the client simply discards the token.
    """
    response.delete_cookie(key="Authorization")
    return {"detail": "Logged out"}
