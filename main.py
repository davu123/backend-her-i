from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Heroi
from pydantic import BaseModel

# Inicializar FastAPI
app = FastAPI()

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

# Schemas para validação com Pydantic
class HeroiCreate(BaseModel):
    name: str
    description: str | None = None
    missao: str | None = None  # Campo para missão
    popularidade: int | None = 0  # Campo para popularidade

class HeroiResponse(HeroiCreate):
    id: int

    class Config:
        orm_mode = True

@app.post("/herois/", response_model=HeroiResponse)
def create_heroi(heroi: HeroiCreate, db: Session = Depends(get_db)):
    db_heroi = Heroi(
        name=heroi.name,
        description=heroi.description,
        missao=heroi.missao,
        popularidade=heroi.popularidade,
    )
    db.add(db_heroi)
    db.commit()
    db.refresh(db_heroi)
    return db_heroi

@app.get("/herois/{heroi_id}", response_model=HeroiResponse)
def read_heroi(heroi_id: int, db: Session = Depends(get_db)):
    heroi = db.query(Heroi).filter(Heroi.id == heroi_id).first()
    if heroi is None:
        raise HTTPException(status_code=404, detail="Herói não encontrado")
    return heroi

@app.put("/herois/{heroi_id}", response_model=HeroiResponse)
def update_heroi(heroi_id: int, heroi: HeroiCreate, db: Session = Depends(get_db)):
    db_heroi = db.query(Heroi).filter(Heroi.id == heroi_id).first()
    if db_heroi is None:
        raise HTTPException(status_code=404, detail="Herói não encontrado")
    db_heroi.name = heroi.name
    db_heroi.description = heroi.description
    db_heroi.missao = heroi.missao
    db_heroi.popularidade = heroi.popularidade
    db.commit()
    db.refresh(db_heroi)
    return db_heroi

@app.delete("/herois/{heroi_id}", status_code=204)
def delete_heroi(heroi_id: int, db: Session = Depends(get_db)):
    db_heroi = db.query(Heroi).filter(Heroi.id == heroi_id).first()
    if db_heroi is None:
        raise HTTPException(status_code=404, detail="Herói não encontrado")
    db.delete(db_heroi)
    db.commit()
