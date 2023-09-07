from sqlalchemy import Column, Integer, String ,ForeignKey,create_engine
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = "sqlite:///contacts.db"  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
def initialize_database():
    Base.metadata.create_all(bind=engine)




class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))  
    last_name = Column(String(50))
    address = Column(String, nullable=True)

    phone_numbers = relationship("PhoneNumber", back_populates="contact")
    email_addresses = relationship("EmailAddress", back_populates="contact")


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    phone_id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    phone_number = Column(String)
    

    
    contact = relationship("Contact", back_populates="phone_numbers")

class EmailAddress(Base):
    __tablename__ = 'email_addresses'

    email_id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    email_address = Column(String, nullable=False)
    email_type = Column(String)

    
    contact = relationship("Contact", back_populates="email_addresses")