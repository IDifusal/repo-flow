from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.db import get_session
from app.schemas.recipe import RecipeCreate, RecipeRead, RecipeRecommendation
from app.services.recipe_service import RecipeService
from app.ai.client import get_ai_client
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
def create_recipe(request: Request, payload: RecipeCreate, session: Session = Depends(get_session)) -> RecipeRead:
    service = RecipeService(session)
    try:
        recipe = service.create_recipe(title=payload.title, description=payload.description)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return RecipeRead.model_validate(recipe)


@router.get("", response_model=list[RecipeRead])
@limiter.limit("100/minute")
def list_recipes(request: Request, session: Session = Depends(get_session)) -> list[RecipeRead]:
    service = RecipeService(session)
    recipes = service.list_recipes()
    return [RecipeRead.model_validate(r) for r in recipes]


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/minute")
def delete_recipe(request: Request, recipe_id: int, session: Session = Depends(get_session)) -> None:
    service = RecipeService(session)
    deleted = service.delete_recipe(recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")

@router.get("/recommendation", response_model=RecipeRecommendation)
@limiter.limit("10/minute")
def recommend_recipe(request: Request, session: Session = Depends(get_session)) -> RecipeRecommendation:
    service = RecipeService(session, ai_client=get_ai_client())
    recipe = service.recommend_recipe()
    if recipe is None:
        return RecipeRecommendation(message="No recipes yet. Create one to get recommendations.")
    return RecipeRecommendation(recipe=RecipeRead.model_validate(recipe))
