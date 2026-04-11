from pydantic import BaseModel
from datetime import datetime
from typing import Literal

StatusType = Literal["applied", "interview", "offer", "rejected","unfit", "fit"]

class JobCreate(BaseModel):
    title : str
    source : str
    company: str
    skills : str
    url : str
    score : float
    status: StatusType = "fit"

class JobUpdateStatus(BaseModel):
    status: StatusType

class JobResponse(BaseModel):
    id: int
    title : str
    source : str
    company: str
    skills : str
    url : str
    score : float
    status: StatusType
    #created_at: datetime

    class Config:
        from_attributes = True
       