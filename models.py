from sqlalchemy import Column, Integer, String
from database import Base

class Heroi(Base):
    __tablename__ = "herois"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    missao = Column(String, nullable=True)  # Nova coluna para missão
    popularidade = Column(Integer, default=0)  # Nova coluna para popularidade
