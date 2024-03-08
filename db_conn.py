from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os


DB_FILE_PATH = "db_assets/data.db"
os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
DB_URL = f"sqlite:///{DB_FILE_PATH}"
engine = create_engine(DB_URL, echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    full_name = Column(String(100))
    user_name = Column(String(100))
    language_code = Column(String(50))
    user_connected = Column(DateTime, default=datetime.now)


class UserPays(Base):
    __tablename__ = "user_pays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    summa = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(100), nullable=False)
    pay_type = Column(Integer)
    pay_data = Column(DateTime, default=datetime.now)
    pay_status = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
