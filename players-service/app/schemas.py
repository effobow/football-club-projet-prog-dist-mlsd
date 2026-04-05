from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str
    position: str
    club_status: str = "active"
    availability: str = "available"


class PlayerUpdate(BaseModel):
    name: str
    position: str
    club_status: str
    availability: str


class PlayerResponse(BaseModel):
    id: int
    name: str
    position: str
    club_status: str
    availability: str

    class Config:
        from_attributes = True