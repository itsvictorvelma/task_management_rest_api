from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

SECRET_KEY = "S5ZcN2Ntazi3k3xkr0Gt53oRQQzNI7RX9yfAK4HRG70"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """hashes a plaintext password using bcrypt"""
    # Convert string password to bytes
    password_bytes = password.encode("utf-8")

    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # Convert byte-hash back to string for database storage
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verifies a candidate password against a stored bcrypt hash"""
    # Convert both string values to bytes for bcrypt comparison
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """generates a signed jwt with an expiration date"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
