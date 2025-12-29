from sqlalchemy import create_engine, Column, Integer, String, Sequence, Boolean, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://opgadmin:secret@localhost:5432/crew"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Roster(Base):
    __tablename__ = 'roster'
    bandit_id = Column(Integer, Sequence('bandit_id_seq'), primary_key=True)
    nickname = Column(String(255), nullable=False)
    bandit_status = Column(Boolean, nullable=False)
    specialization = Column(Text)
    bandit_level = Column(Integer)
    contacts = Column(Text)
    appearance_date = Column(Date)

class Bank(Base):
    __tablename__ = 'bank'
    bank_id = Column(Integer, Sequence('bank_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    security_level = Column(Integer)
    daily_income = Column(Integer)
    attractiveness = Column(Integer)

class Robbery(Base):
    __tablename__ = 'robbery'
    robbery_id = Column(Integer, Sequence('robbery_id_seq'), primary_key=True)
    bandit_id = Column(Integer, ForeignKey('roster.bandit_id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('bank.bank_id'), nullable=False) 
    robbery_date = Column(Date, nullable=False)
    bandit_outcome = Column(Boolean, nullable=False) 
    share = Column(Integer) 
    action_score = Column(Integer)