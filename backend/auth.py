from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import hashlib

# -----------------------------
# 🔹 Load Environment Variables
# -----------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# -----------------------------
# 🔐 Password Hashing Setup
# -----------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -----------------------------
# 🔐 Hash Password (SAFE ✅)
# -----------------------------
def hash_password(password: str) -> str:
    # Debug (optional)
    print("Hashing Password length:", len(password))

    # ✅ Step 1: SHA256 (removes 72 byte limit issue)
    sha_password = hashlib.sha256(password.encode()).hexdigest()

    # ✅ Step 2: bcrypt
    return pwd_context.hash(sha_password)


# -----------------------------
# 🔐 Verify Password
# -----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    print("Verifying Password length:", len(plain_password))

    sha_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha_password, hashed_password)


# -----------------------------
# 🪙 Create Access Token
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# -----------------------------
# 🔍 Verify Token
# -----------------------------
def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None