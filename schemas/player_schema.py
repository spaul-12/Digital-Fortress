from pydantic import BaseModel

class registerToken(BaseModel):
    token : str
    type : str