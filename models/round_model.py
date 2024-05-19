from services.database import Base
from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Relationship
from datetime import datetime

class Round(Base):
    __tablename__ = "round"

    roundNumber = mapped_column(Integer,primary_key=True,index=True)
    question = mapped_column(String(750))
    answer = mapped_column(String(200))
    imagePath = mapped_column(String(200))
    audioPath = mapped_column(String(200))
    clues = Relationship("Clue",back_populates= "round", cascade="all, delete")

class Clue(Base):
    __tablename__ = "clue"

    id = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    roundNumber = mapped_column(Integer,ForeignKey("round.roundNumber"))
    question = mapped_column(String(750))
    audioPath = mapped_column(String(200))
    imagePath = mapped_column(String(200))
    answer = mapped_column(String(200))
    round = Relationship("Round",back_populates="clues")


class Duration(Base):
    __tablename__ = "duration"

    id = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    startTime = mapped_column(DateTime,default=datetime.now())
    endTime = mapped_column(DateTime,default=datetime.now())
    leaderboardFreeze = mapped_column(Boolean,default=False)
    leaderboardHide = mapped_column(Boolean,default=False)
    maxQuestions = mapped_column(Integer,default=20)

