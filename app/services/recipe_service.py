from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.repositories.recipe_repo import RecipeRepository


class RecipeService:
    def __init__(self, session: Session) -> None:
        self.repo = RecipeRepository(session)

    def create_recipe(self, title: str, description: str | None) -> Recipe:
        title_clean = title.strip()
        if not title_clean:
            raise ValueError("title is required")
        return self.repo.create(title=title_clean, description=description)

    def list_recipes(self) -> list[Recipe]:
        return self.repo.list()

    def delete_recipe(self, recipe_id: int) -> bool:
        return self.repo.delete(recipe_id)

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        return self.repo.get(recipe_id)
