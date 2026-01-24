from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], Deprecated="auto")


# hash password
def hashpassword(passwprd: str):
    return password_context.hash(passwprd)


# password veryfied
def passwordVeryfied(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)
print("Password")
