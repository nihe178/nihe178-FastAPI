from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.POSTGRES_SVR_USR}:{settings.POSTGRES_SVR_PWD}@{settings.POSTGRES_SVR_URL}:{settings.POSTGRES_SVR_PRT}/{settings.POSTGRES_SVR_DB}'
#print(settings.POSTGRES_SVR_DB)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='apidb',user='postgres',password='!!C0mpaq2532', cursor_factory=RealDictCursor)
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("error", error) 
#         time.sleep(2)