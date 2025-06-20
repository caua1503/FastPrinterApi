import random
import string
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import Config

pwd_context = PasswordHash(hashers=["argon2"]).recommended()


def get_password_hash(password: str, code_hash: str) -> str:
    password += code_hash
    return pwd_context.hash(password)


def verify_password(password: str, code_hash: str, hashed_password: str) -> bool:
    password += code_hash
    return pwd_context.verify(password, hashed_password)


def generate_random_code(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(length))
    return code


def generate_api_key() -> str:
    api_key = f"api_key_{generate_random_code(64)}"
    return api_key


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, generate_random_code(32), algorithm=Config().JWT_ALGORITHM)
    return encoded_jwt
