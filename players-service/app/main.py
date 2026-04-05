from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Player
from .schemas import PlayerCreate, PlayerUpdate, PlayerResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Players Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Players service is running"}


@app.get("/players", response_model=list[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


@app.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.post("/players", response_model=PlayerResponse, status_code=201)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    new_player = Player(
        name=player.name,
        position=player.position,
        club_status=player.club_status,
        availability=player.availability
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player


@app.put("/players/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.name = player_update.name
    player.position = player_update.position
    player.club_status = player_update.club_status
    player.availability = player_update.availability

    db.commit()
    db.refresh(player)
    return player


@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()
    return {"message": "Player deleted successfully"}