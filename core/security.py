from passlib.context import CryptContext
from secrets import token_hex


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def create_hash_token(password) -> str:
    while True:
        token = pwd_context.hash(password)
        if '/' in token:
            continue
        else:
            return token


def create_access_token() -> str:
    return token_hex(32)


def verify_hash_token(password, password_hash) -> bool:
    return pwd_context.verify(password, password_hash)


def hash_passwd(password) -> str:
    return pwd_context.hash(password)


def verify_hash_passwd(passwd, password_hash):
    return pwd_context.verify(passwd, password_hash)
    
    