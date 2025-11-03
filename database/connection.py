import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def obtener_db():
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()
