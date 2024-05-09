from services.database import Base
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import mapped_column

class Player(Base):
    __tablename__ = "player"

    id = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name = mapped_column(String(200))
    fullName = mapped_column(String(200))
    email = mapped_column(String(254))
    imageLink = mapped_column(String(200))
    score = mapped_column(Integer,default = 0)
    roundNo = mapped_column(Integer,default = 1)
    currentHints = mapped_column(String(200))
    submitTime = mapped_column(DateTime)
    isStaff = mapped_column(Boolean,default=False)
