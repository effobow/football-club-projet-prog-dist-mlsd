from sqlalchemy import Column, Integer, String
from .database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    club_status = Column(String, nullable=False, default="active")  
    availability = Column(String, nullable=False, default="available")