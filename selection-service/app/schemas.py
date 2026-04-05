from pydantic import BaseModel
from typing import List

class SelectionCreate(BaseModel):
    match_name: str
    match_date: str
    player_ids: List[int]

class SelectionResponse(BaseModel):
    id: int
    match_name: str
    match_date: str
    player_ids: List[int]

    class Config:
        from_attributes = True