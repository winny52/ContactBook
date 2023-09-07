from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ContactBook.models.contact import Base
from ContactBook.models.emailaddresses import Base
from ContactBook.models.phonenumber import Base


DATABASE_URL = "sqlite:///contacts.db"  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    Base.metadata.create_all(bind=engine)


