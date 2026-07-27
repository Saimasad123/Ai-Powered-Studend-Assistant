from datetime import datetime, timedelta
from typing import Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expire, 'sub': subject}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(sub=int(payload.get('sub')), email=payload.get('email'))
    except JWTError:
        return None
