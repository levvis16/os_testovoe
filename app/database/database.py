from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv() 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass
#подумать о сессиях и времени жизни хранения