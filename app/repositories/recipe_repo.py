from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.recipe import Recipe


class RecipeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, title: str, description: str | None) -> Recipe:
        recipe = Recipe(title=title, description=description)
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def list(self) -> list[Recipe]:
        result = self.session.execute(select(Recipe).order_by(Recipe.created_at.desc(), Recipe.id.desc()))
        return list(result.scalars().all())

    def get(self, recipe_id: int) -> Recipe | None:
        return self.session.get(Recipe, recipe_id)

    def delete(self, recipe_id: int) -> bool:
        recipe = self.get(recipe_id)
        if recipe is None:
            return False
        self.session.delete(recipe)
        self.session.commit()
        return True
