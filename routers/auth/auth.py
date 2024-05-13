from google.oauth2 import id_token
from google.auth.transport import requests
from services.utils import get_db_session
from fastapi import APIRouter,Depends,status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.player_model import Player
from config import config
from utils import createAccessToken
from schemas import player_schema

router  = APIRouter()

async def getUserId(email: str,db: AsyncSession):
    query = select(Player).where(Player.email == email)
    res = await db.execute(query)
    player = res.scalars().first()
    return (player.id if player is not None else None)


def verifyGoogleToken(token: str):
    try:
        CLIENT_ID = config.get("CLIENT_ID")
        token = token.strip("\"")
        idinfo = id_token.verify_oauth2_token(token,requests.Request(),CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        return {
            "email": idinfo['email'],
            "fullName": idinfo['name'],
            "imageLink": idinfo['picture'],
            "status": 200
        }

    except Exception as error:
        return {"status":404,"message":error}

@router.post("/auth/register")
async def register(req:player_schema.registerToken, db: AsyncSession = Depends(get_db_session)):
    if req.type == "1":
        res = verifyGoogleToken(req.token)

    if res['status'] == 404:
        raise HTTPException(status_code=404,detail="Invalid token")
    else:
        userId = await getUserId(res['email'],db)

        if userId is None:
            newUser = Player(fullName=res['fullName'],email=res['email'],imageLink=res['imageLink'])
            db.add(newUser)
            await db.commit()
            await db.refresh(newUser)

            accessToken = createAccessToken(newUser.id)
            return {
                "token":accessToken,
                "status":200
            }
        else :
            accessToken = createAccessToken(userId)
            return {
                "token":accessToken,
                "status":200
            }




    