from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import validates, relationship
from passlib.context import CryptContext
from app.database import Base

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    recipes = relationship("Recipe", back_populates="owner")

    @validates("password")
    def hash_password(self, key, password):
        return pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    ingredients = Column(
        Text, nullable=False
    )  # Store ingredients as a JSON string or comma-separated
    instructions = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Link to user

    owner = relationship("User", back_populates="recipes")
