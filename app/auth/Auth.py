from datetime import datetime
import bcrypt
import jwt

from app.env.Env import get_settings


settings = get_settings()

class AuthService:

    @classmethod
    def encrypt_password(cls, password:str) -> str :
        salt = bcrypt.gensalt(6)
        pass_encrypted = bcrypt.hashpw(
            password= bytes(password , "UTF-8"),
            salt = salt
        )
        return str(pass_encrypted , "UTF-8")

    @classmethod
    def validate_password(cls, password:str, db_hash_pass : str) -> bool :
        b_pass  = bytes(password,"UTF-8")
        db_pass = bytes(db_hash_pass,"UTF-8")
        return bcrypt.checkpw(
            password= b_pass,
            hashed_password= db_pass
        )
    
    @classmethod
    def generate_jwt( cls ,payload : dict[str,any] ) -> str :
        time_unix = int(datetime.utcnow().timestamp())
        payload["exp"] = time_unix + 60
        token : str = jwt.encode(payload , settings.my_secret)
        return token






