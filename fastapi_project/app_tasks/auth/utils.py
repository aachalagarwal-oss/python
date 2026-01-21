from passlib.context import CryptContext


pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')



class Hash:
    def hashit(password_hashed:str):
        return pwd_cxt.hash(password_hashed)
    
    