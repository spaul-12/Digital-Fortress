from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.round_model import Round,Duration,Clue
from models.player_model import Player

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

async def getroundDetails(roundNumber: int, db: AsyncSession):
    query = select(Round).where(Round.roundNumber == roundNumber)
    res = await db.execute(query)
    round = res.scalars().first()
    return round

async def getPlayerDetails(userId: int, db: AsyncSession):
    query = select(Player).where(Player.id == userId)
    res = await db.execute(query)
    player = res.scalars().first()
    return player