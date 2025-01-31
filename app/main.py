from fastapi import FastAPI
from app.database import engine
from app import models

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Cookbooked!"}
