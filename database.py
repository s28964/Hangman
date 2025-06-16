from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///users.db') #tworzy silnik połączenia z bazą danych
Session = sessionmaker(bind=engine) #Tworzy klasę session, którą łączymy z silnikiem bazodanowym
session = Session() #instacja klasy Session

def init_db():
    Base.metadata.create_all(engine) #Funkcja, która tworzy wszystkie tabele na podstawie pliku models.py jeżeli jeszcze nie są stworzone