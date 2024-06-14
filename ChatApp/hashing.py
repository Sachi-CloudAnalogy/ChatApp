import bcrypt

class Hash():
    @staticmethod
    def bcrypt(password: str) -> str:
        hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hash.decode('utf-8')
    
    @staticmethod
    def verify(hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

