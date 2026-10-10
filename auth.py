import bcrypt
import hashlib


def _prepare_password(password: str) -> bytes:
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest().encode("utf-8")


def hash_password(password: str) -> str:
    password_bytes = _prepare_password(password)

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        _prepare_password(plain_password),
        hashed_password.encode("utf-8")
    )