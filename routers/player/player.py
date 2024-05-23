from services.utils import get_db_session
from fastapi import APIRouter,Depends,status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.player_model import Player
from models.round_model import Round,Duration,Clue
from schemas import round_schemas
from config import config
from middlewares import auth_bearer
from datetime import datetime
from .utils import getDuration, getPlayerDetails, getRoundNumber, getroundDetails

router = APIRouter()



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
    


@router.post('/checkRound')
async def checkRound(response: round_schemas.PlayerResponse, db: AsyncSession = Depends(get_db_session), dependencies = Depends(auth_bearer.JWTBearer())):

    userId = dependencies['id']
    duration = await getDuration(db)

    currTime = datetime.now()
    if duration.startTime < currTime and currTime < duration.endTime:

        player = await getPlayerDetails(userId, db)
        round = await getroundDetails(response.roundNumber, db)

        if round.answer == response.answer:
            player.roundNo += 1
            player.submitTime = datetime.now()
            if duration.leaderboardFreeze:
                db.add(player)
                await db.commit()
                return {"message":"correct answer"}
            
            else :
                player.score += 10
                db.add(player)
                await db.commit()
                return {"message": "correct answer"}
        
        else:
            return {"message": "wrong answer"}


