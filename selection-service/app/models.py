from sqlalchemy import Column, Integer, String
from .database import Base

class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)
    match_name = Column(String, nullable=False)
    match_date = Column(String, nullable=False)
    player_ids = Column(String, nullable=False)