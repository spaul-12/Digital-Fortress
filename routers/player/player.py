from services.utils import get_db_session
from fastapi import APIRouter,Depends,status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.player_model import Player
from models.round_model import Round,Duration,Clue
from config import config
from middlewares import auth_bearer
from datetime import datetime

router = APIRouter()


async def getRoundNumber(id: int, db: AsyncSession):
    query = select(Player).where(Player.id == id)
    res = await db.execute(query)
    player = res.scalars().first()
    return player.roundNo

async def getDuration(db: AsyncSession):
    query = select(Duration)
    res = await db.execute(query)
    duration  = res.scalars().first()
    return duration


@router.get('/getRound')
async def getRound(dependencies= Depends(auth_bearer.JWTBearer()),db: AsyncSession = Depends(get_db_session)):

    userId = dependencies['id']
    duration = await getDuration(db)
    
    currTime = datetime.now()
    if duration.startTime < currTime and currTime < duration.endTime:

        roundNo = await getRoundNumber(userId, db)
        if duration.maxQuestions >= roundNo:
            query = select(Round).where(Round.roundNumber == roundNo)
            res = await db.execute(query)
            details = res.scalars().first()
            return {
                "roundNumber": details.roundNumber,
                "question" : details.question,
                "imagePath" : details.imagePath,
                "audioPath" : details.audioPath
            }
        
        else:
            raise HTTPException(status_code=404,detail="Max round reached")
        
    else:
        raise HTTPException(status_code=410,detail="Game ended")    
    



