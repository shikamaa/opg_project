from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from schemas import *
from opg_db import engine, Base, get_db
from models import Roster, Bank, Robbery

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg": "ok"}

@app.post('/roster/', response_model=RosterResponse, status_code=201)
def create_roster(roster: RosterBase, db: Session = Depends(get_db)):
    db_roster = Roster(**roster.dict())
    db.add(db_roster)
    db.commit()
    db.refresh(db_roster)
    return db_roster

@app.get('/roster/', response_model=List[RosterResponse])
def read_roster(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rosters = db.query(Roster).offset(skip).limit(limit).all()
    return rosters

@app.get('/roster/{bandit_id}', response_model=RosterResponse)
def read_roster_by_id(bandit_id: int, db: Session = Depends(get_db)):
    roster = db.query(Roster).filter(Roster.bandit_id == bandit_id).first()
    if not roster:
        raise HTTPException(status_code=404, detail="bandit not found")
    return roster

@app.put('/roster/{bandit_id}', response_model=RosterResponse)
def update_roster(bandit_id: int, roster: RosterBase, db: Session = Depends(get_db)):
    db_roster = db.query(Roster).filter(Roster.bandit_id == bandit_id).first()
    if not db_roster:
        raise HTTPException(status_code=404, detail="bandit not found")
    
    for key, value in roster.dict().items():
        setattr(db_roster, key, value)
    
    db.commit()
    db.refresh(db_roster)
    return db_roster

@app.delete('/roster/{bandit_id}')
def delete_roster(bandit_id: int, db: Session = Depends(get_db)):
    db_roster = db.query(Roster).filter(Roster.bandit_id == bandit_id).first()
    if not db_roster:
        raise HTTPException(status_code=404, detail="bandit not found")
    
    db.delete(db_roster)
    db.commit()
    return {"message": "bandit deleted"}

@app.post('/bank/', response_model=BankResponse, status_code=201)
def create_bank(bank: BankBase, db: Session = Depends(get_db)):
    db_bank = Bank(**bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@app.get('/bank/', response_model=List[BankResponse])
def read_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    banks = db.query(Bank).offset(skip).limit(limit).all()
    return banks

@app.get('/bank/{bank_id}', response_model=BankResponse)
def read_bank_by_id(bank_id: int, db: Session = Depends(get_db)):
    bank = db.query(Bank).filter(Bank.bank_id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@app.put('/bank/{bank_id}', response_model=BankResponse)
def update_bank(bank_id: int, bank: BankBase, db: Session = Depends(get_db)):
    db_bank = db.query(Bank).filter(Bank.bank_id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    for key, value in bank.dict().items():
        setattr(db_bank, key, value)
    
    db.commit()
    db.refresh(db_bank)
    return db_bank

@app.delete('/bank/{bank_id}')
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    db_bank = db.query(Bank).filter(Bank.bank_id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    db.delete(db_bank)
    db.commit()
    return {"message": "bank deleted"}

@app.post('/robbery/', response_model=RobberyResponse, status_code=201)
def create_robbery(robbery: RobberyBase, db: Session = Depends(get_db)):
    bandit = db.query(Roster).filter(Roster.bandit_id == robbery.bandit_id).first()
    if not bandit:
        raise HTTPException(status_code=404, detail="bandit not found")
    
    bank = db.query(Bank).filter(Bank.bank_id == robbery.bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="bank not found")
    
    db_robbery = Robbery(**robbery.dict())
    db.add(db_robbery)
    db.commit()
    db.refresh(db_robbery)
    return db_robbery

@app.get('/robbery/', response_model=List[RobberyResponse])
def read_robberies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    robberies = db.query(Robbery).offset(skip).limit(limit).all()
    return robberies

@app.get('/robbery/{robbery_id}', response_model=RobberyResponse)
def read_robbery_by_id(robbery_id: int, db: Session = Depends(get_db)):
    robbery = db.query(Robbery).filter(Robbery.robbery_id == robbery_id).first()
    if not robbery:
        raise HTTPException(status_code=404, detail="robbery not found")
    return robbery

@app.put('/robbery/{robbery_id}', response_model=RobberyResponse)
def update_robbery(robbery_id: int, robbery: RobberyBase, db: Session = Depends(get_db)):
    db_robbery = db.query(Robbery).filter(Robbery.robbery_id == robbery_id).first()
    if not db_robbery:
        raise HTTPException(status_code=404, detail="robbery not found")
    
    for key, value in robbery.dict().items():
        setattr(db_robbery, key, value)
    
    db.commit()
    db.refresh(db_robbery)
    return db_robbery

@app.delete('/robbery/{robbery_id}')
def delete_robbery(robbery_id: int, db: Session = Depends(get_db)):
    db_robbery = db.query(Robbery).filter(Robbery.robbery_id == robbery_id).first()
    if not db_robbery:
        raise HTTPException(status_code=404, detail="robbery not found")
    
    db.delete(db_robbery)
    db.commit()
    return {"message": "robbery deleted"}


from sqlalchemy import func

@app.get('/roster/filter/', response_model=List[RosterResponse])
def filter_roster(specialization: str, min_level: int = 1, db: Session = Depends(get_db)):
    results = db.query(Roster).filter(
        Roster.specialization == specialization,
        Roster.bandit_level >= min_level
    ).all()
    return results


@app.get('/robbery/details/', response_model=List[dict])
def robbery_details(db: Session = Depends(get_db)):
    results = db.query(
        Robbery.robbery_id,
        Roster.nickname.label('bandit_name'),
        Bank.name.label('bank_name'),
        Robbery.robbery_date,
        Robbery.share
    ).join(Roster, Robbery.bandit_id == Roster.bandit_id)\
     .join(Bank, Robbery.bank_id == Bank.bank_id)\
     .all()
    
    return [dict(r._asdict()) for r in results]

@app.put('/roster/increase_score/')
def increase_score(db: Session = Depends(get_db)):
    updated = db.query(Roster)\
        .filter(Roster.bandit_level > 7, Roster.specialization == 'hacker')\
        .update({Roster.score: Roster.score + 10}, synchronize_session=False)
    
    db.commit()
    return {"updated": updated}

@app.get('/robbery/summary/', response_model=List[dict])
def robbery_summary(db: Session = Depends(get_db)):
    results = db.query(
        Robbery.bandit_id,
        func.sum(Robbery.share).label('total_share')
    ).group_by(Robbery.bandit_id).all()
    
    return [dict(r._asdict()) for r in results]

@app.get('/roster/sorted/', response_model=List[RosterResponse])
def sorted_roster(order: str = 'desc', db: Session = Depends(get_db)):
    query = db.query(Roster)
    if order == 'asc':
        query = query.order_by(Roster.score.asc())
    else:
        query = query.order_by(Roster.score.desc())
    
    return query.all()
