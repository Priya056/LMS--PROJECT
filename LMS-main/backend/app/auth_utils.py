from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(sub: str) -> str:
    s = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=s.access_token_expire_minutes)
    return jwt.encode({"sub": sub, "exp": expire}, s.secret_key, algorithm=s.algorithm)


def decode_token(token: str) -> str | None:
    try:
        s = get_settings()
        payload = jwt.decode(token, s.secret_key, algorithms=[s.algorithm])
        sub = payload.get("sub")
        return str(sub) if sub else None
    except JWTError:
        return None
