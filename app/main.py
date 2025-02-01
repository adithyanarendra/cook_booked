from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import engine
from app import crud, models, schemas
from app.database import SessionLocal
from app.recipe_routes import recipe_routes
import app.auth as auth
from datetime import timedelta
from app import models

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(recipe_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Cookbooked!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user


@app.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = auth.get_user(db, username=form_data.username)

    if not db_user or not auth.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile/")
def get_profile(
    username: str = Depends(auth.get_current_user), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email,
    }


@app.put("/profile/update/")
def update_profile(
    user_update: schemas.UserUpdate,
    username: str = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = user_update.email or user.email
    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "user": {"username": user.username, "email": user.email},
    }
