import hashlib
import secrets
import string
from datetime import UTC, datetime

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_case_id() -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%d")
    suffix = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"CASE-{stamp}-{suffix}"


def generate_access_key() -> str:
    alphabet = string.ascii_uppercase + string.digits
    chunks = ["".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(3)]
    return "-".join(chunks)


def hash_access_key(access_key: str) -> str:
    return pwd_context.hash(access_key)


def verify_access_key(access_key: str, hashed_access_key: str) -> bool:
    return pwd_context.verify(access_key, hashed_access_key)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

