from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from authentication.database import Base

class Leaderboard(Base):
    __tablename__ = "redisusage"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    score = Column(Integer)
