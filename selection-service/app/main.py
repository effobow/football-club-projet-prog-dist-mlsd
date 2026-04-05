from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Selection
from .schemas import SelectionCreate, SelectionResponse

import requests

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Selection Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Selection service is running"}


@app.get("/selections", response_model=list[SelectionResponse])
def get_selections(db: Session = Depends(get_db)):
    selections = db.query(Selection).all()
    result = []

    for s in selections:
        result.append({
            "id": s.id,
            "match_name": s.match_name,
            "match_date": s.match_date,
            "player_ids": list(map(int, s.player_ids.split(",")))
        })

    return result


@app.post("/selections", response_model=SelectionResponse)
def create_selection(selection: SelectionCreate, db: Session = Depends(get_db)):

    # 🔥 Vérification des joueurs via players-service
    for player_id in selection.player_ids:
        response = requests.get(f"http://players-service:8000/players/{player_id}")

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Player {player_id} not found"
            )

        player = response.json()

        if player["availability"] != "available":
            raise HTTPException(
                status_code=400,
                detail=f"Player {player_id} not available"
            )

    players_str = ",".join(map(str, selection.player_ids))

    new_selection = Selection(
        match_name=selection.match_name,
        match_date=selection.match_date,
        player_ids=players_str
    )

    db.add(new_selection)
    db.commit()
    db.refresh(new_selection)

    return {
        "id": new_selection.id,
        "match_name": new_selection.match_name,
        "match_date": new_selection.match_date,
        "player_ids": selection.player_ids
    }


@app.delete("/selections/{selection_id}")
def delete_selection(selection_id: int, db: Session = Depends(get_db)):
    selection = db.query(Selection).filter(Selection.id == selection_id).first()

    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")

    db.delete(selection)
    db.commit()

    return {"message": "Selection deleted"}