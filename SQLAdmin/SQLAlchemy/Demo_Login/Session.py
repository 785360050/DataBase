# from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from Engine import engine

session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
