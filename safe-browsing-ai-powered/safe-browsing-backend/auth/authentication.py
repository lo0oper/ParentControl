import dotenv
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
import jwt
import os
import datetime
import bcrypt

from log.logger import logger

dotenv.load_dotenv()
log = logger


class Authentication():
    def __init__(self):
        self.secret_key = os.getenv('secret')
        self.algorithm = os.getenv('algorithm')
        log.info(f"secret :{self.secret_key} and algo:{self.algorithm}")
        return 
    

    def getjwttoken(self,user_id:str,expiry_in_seconds:int):
            payload = {
                    "user_id":user_id,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expiry_in_seconds)
            }
            encoded = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            log.debug(f'encoded data for :${payload.get("exp")} and userId:${user_id}')
            return encoded


    def decodejwttoken(self,token,user_id):
          user_id = jwt.decode(token,self.secret_key,self.algorithm)['user_id']
          return user_id
    
    
    def authenticate(self,user_id,token):
        is_authenticated = False
        try:
            user_id = jwt.decode(token, self.secret_key, self.algorithm)['user_id']
            if user_id:
                is_authenticated = True
            return is_authenticated
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not authorized , please provide correct token."
            )
            
    

    # Utility function to hash password
    def hash_password(self,password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Utility function to verify password
    def verify_password(self,plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))