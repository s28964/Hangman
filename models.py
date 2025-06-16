from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() #Tworzy klasę bazową, z której będą dziedziczyć wszystkie modele (wymóg SQLAlchemy)

class User(Base):
    __tablename__ = 'users' #Definiuje tabelę users w bazie danych

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)

class Word(Base):
    __tablename__ = 'words' #Definiuje tabelę words w bazie danych

    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)