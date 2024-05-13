import jwt
from datetime import datetime, timedelta
from config import config

def createAccessToken(id: int):
    try:
        expireDelta = datetime.now() + timedelta(minutes=int(config.get('ACCESS_TOKEN_EXPIRE_MINUTES')))
        toEncode = {
            "exp":expireDelta,
            "id":id
        }

        encodedJWT = jwt.encode(toEncode,config.get('JWT_SECRET_KEY'),config.get('ALGORITHM'))
        return encodedJWT
    except Exception:
        return None

def decodeJWT(jwtToken: str):
    try:
        payload = jwt.decode(jwtToken,config.get('JWT_SECRET_KEY'),config.get('ALGORITHM'))
        return payload
    except jwt.exceptions.InvalidKeyError:
        return None
    