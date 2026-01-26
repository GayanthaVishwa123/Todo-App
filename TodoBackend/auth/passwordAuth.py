from passlib.context import CryptContext

<<<<<<< HEAD
# Create a CryptContext for password hashing and verification
=======
>>>>>>> TodoTst_and_Auth/dev
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password
def hash_password(password: str):
    return password_context.hash(password)


# Verify password
def password_verified(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)
