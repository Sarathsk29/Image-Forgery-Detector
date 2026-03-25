import hashlib
import secrets
import string
from datetime import UTC, datetime

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def generate_case_id() -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%d")
    suffix = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"CASE-{stamp}-{suffix}"


def generate_access_key() -> str:
    alphabet = string.ascii_uppercase + string.digits
    chunks = ["".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(3)]
    return "-".join(chunks)


def hash_access_key(access_key: str) -> str:
    # bcrypt has a 72-byte input limit; truncate UTF-8 bytes to avoid errors
    b = access_key.encode("utf-8")
    if len(b) > 72:
        b = b[:72]
    return pwd_context.hash(b)


def verify_access_key(access_key: str, hashed_access_key: str) -> bool:
    b = access_key.encode("utf-8")
    if len(b) > 72:
        b = b[:72]
    return pwd_context.verify(b, hashed_access_key)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

