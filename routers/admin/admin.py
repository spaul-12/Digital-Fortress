from services.utils import get_db_session
from fastapi import APIRouter,Depends,status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import round_schemas
from middlewares import auth_bearer
from models.player_model import Player
from models.round_model import Duration

router = APIRouter()

async def isStaff(userId: int, db: AsyncSession):
    query = select(Player).where(Player.id == userId)
    res = await db.execute(query)
    player = res.scalars().first()
    return player.isStaff

@router.post('/addDuration')
async def addDuration(details: round_schemas.GameDuration, db: AsyncSession = Depends(get_db_session), dependencies = Depends(auth_bearer.JWTBearer())):
    userId = dependencies['id']
    staff = await isStaff(userId, db)
    if not staff:
        raise HTTPException(status_code=403,detail='Unauthorised')
    
    newDuration = Duration(startTime = details.startTime, endTime = details.endTime, leaderboardFreeze = details.leaderboardFreeze, leaderboardHide = details.leaderboardHide, maxQuestions = details.maxQuestions)

    db.add(newDuration)
    await db.commit()
    await db.refresh(newDuration)

    return {"status":200,"message":"successfully added"}

    