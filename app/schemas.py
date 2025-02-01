from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: str
    instructions: str


class RecipeCreate(RecipeBase):
    pass  # Same as RecipeBase, but useful for clarity


class RecipeUpdate(RecipeBase):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None


class RecipeResponse(RecipeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
