import pymysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    url=settings.CONNECTION_URL,
    echo=False
)

Session: sessionmaker = sessionmaker(bind=engine)
