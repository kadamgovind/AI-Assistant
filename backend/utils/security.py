from passlib.context import CryptContext

# -----------------------------
# 🔐 Password Hashing Config
# -----------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -----------------------------
# 🔒 Hash Password
# -----------------------------
def hash_password(password: str) -> str:
    """
    Convert plain password to hashed password
    (Use during signup)
    """
    if not password:
        raise ValueError("Password cannot be empty")

    return pwd_context.hash(password)


# -----------------------------
# ✅ Verify Password
# -----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare plain password with hashed password
    (Use during login)
    """
    if not plain_password or not hashed_password:
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False