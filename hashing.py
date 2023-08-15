from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

# pwd_cxt.verify(request.password, user.password)
class Hash():
    def bcrypt(password: str):
        # hashed_pwd = pwd_cxt.hash(password)
        return pwd_cxt.hash(password)