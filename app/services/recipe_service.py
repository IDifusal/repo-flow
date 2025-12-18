from sqlalchemy.orm import Session
from app.ai.client import AIClient
from app.models.recipe import Recipe
from app.repositories.recipe_repo import RecipeRepository


class RecipeService:
    def __init__(self, session: Session, ai_client: AIClient | None = None) -> None:
        self.repo = RecipeRepository(session)
        self.ai_client = ai_client

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

    def recommend_recipe(self) -> Recipe | None:
        recipes = self.repo.list()
        if not recipes:
            return None

        if self.ai_client is None:
            return recipes[0]

        try:
            recommended_id = self.ai_client.recommend(recipes)
        except Exception:
            return recipes[0]

        if recommended_id is None:
            return recipes[0]

        recommended = self.repo.get(recommended_id)
        return recommended or recipes[0]
