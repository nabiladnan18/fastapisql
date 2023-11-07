from passlib.context import CryptContext

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hashed(password: str):
    return PWD_CONTEXT.hash(password)
