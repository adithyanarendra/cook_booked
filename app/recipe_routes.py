from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.main import get_db
from app.auth import get_current_user  # Assume you have this function

router = APIRouter()


@router.post("/recipes/", response_model=schemas.RecipeResponse)
def create_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return crud.create_recipe(db, recipe, user.id)


@router.get("/recipes/", response_model=list[schemas.RecipeResponse])
def get_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip, limit)


@router.get("/recipes/{recipe_id}", response_model=schemas.RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/recipes/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if db_recipe.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this recipe")
    
    return crud.update_recipe(db, recipe_id, recipe)


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if db_recipe.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this recipe")

    success = crud.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete recipe")
    
    return {"message": "Recipe deleted successfully"}
