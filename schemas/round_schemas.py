from pydantic import BaseModel
from typing import Union
from datetime import datetime


class Question(BaseModel):
    roundNumber : int
    question : str
    answer : str
    imagePath : Union[str, None] = None
    audioPath : Union[str, None] = None

class GameDuration(BaseModel):
    startTime : datetime
    endTime : datetime
    leaderboardFreeze : bool
    leaderboardHide : bool
    maxQuestions : int


class PlayerResponse(BaseModel):
    roundNumber: int
    answer : str