from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import config

engine = create_async_engine(config.get("SQLALCHEMY_DATABASE_URL"))
sessionLocal = async_sessionmaker(bind=engine,autocommit=False)
Base = declarative_base()  # model base class

