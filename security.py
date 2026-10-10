from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


# Secret key used to sign JWT tokens
SECRET_KEY = "ecommerce-api-secret-key-change-later"

# Algorithm used for JWT
ALGORITHM = "HS256"

# Token validity
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify JWT token and return its payload.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None