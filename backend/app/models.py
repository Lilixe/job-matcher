from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class JobApplication(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String,nullable=False)
    title = Column(String,nullable=False)
    company = Column(String, nullable=False)
    url = Column(String,nullable=False)
    skills = Column(String)
    score = Column(Float,nullable=False)
    status = Column(String, nullable=False, default="fit")
    created_at = Column(DateTime, default=datetime.utcnow)