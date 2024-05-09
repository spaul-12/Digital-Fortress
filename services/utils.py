from services.database import engine,sessionLocal,Base
from models import player_model

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def db_close():
    if engine is None:
        raise Exception("Database engine is not initialized")
    
    await engine.dispose()


async def get_db_session():
    if sessionLocal is None:
        raise Exception("Database session is not initialized")
    
    session = sessionLocal()
    try:
        yield session
    finally:
        await session.close()