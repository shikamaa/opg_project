from sqlalchemy import Column, Integer, String, Sequence, Boolean, Text, Date
from .database import Base
import uvicorn


class Roser(Base):
    __tablename__ = 'Roaster'
    bandit_id = Column(Integer,Sequence('bandit_id_seq'), primary_key=True)
    nickname = Column(String(255), nullable=False)
    bandit_status = Column(Boolean, nullable=False)
    specialization = Column(Text)
    bandit_level = Column(Integer)
    contacts = Column(Text)
    appearance_date = Column(Date)





"""
    bandit_id BIGSERIAL PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL,
    bandit_status BOOLEAN NOT NULL,
    specialization TEXT,
    bandit_level INT,
    contacts TEXT,
    appearance_date DATE
    """
