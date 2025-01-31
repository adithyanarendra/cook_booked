from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from passlib.context import CryptContext
from app.database import Base

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    @validates('password')
    def hash_password(self, key, password):
        return pwd_context.hash(password)
    
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)
