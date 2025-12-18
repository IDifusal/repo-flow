import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import QueryDepthLimiter
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.recipe_service import RecipeService
from app.ai.client import get_ai_client
from app.api.graphql.types import RecipeType
from app.models.recipe import Recipe


def to_recipe_type(recipe: Recipe) -> RecipeType:
    return RecipeType(
        id=recipe.id,
        title=recipe.title,
        description=recipe.description,
        created_at=recipe.created_at,
    )


@strawberry.type
class Query:
    @strawberry.field
    def recipes(self, info) -> list[RecipeType]:
        session: Session = next(get_session())
        service = RecipeService(session)
        recipes = service.list_recipes()
        session.close()
        return [to_recipe_type(r) for r in recipes]

    @strawberry.field
    def recommend_recipe(self, info) -> RecipeType | None:
        session: Session = next(get_session())
        service = RecipeService(session, ai_client=get_ai_client())
        recipe = service.recommend_recipe()
        session.close()
        if recipe is None:
            return None
        return to_recipe_type(recipe)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_recipe(self, title: str, description: str | None = None) -> RecipeType:
        session: Session = next(get_session())
        service = RecipeService(session)
        recipe = service.create_recipe(title=title, description=description)
        session.close()
        return to_recipe_type(recipe)

    @strawberry.mutation
    def delete_recipe(self, recipe_id: int) -> bool:
        session: Session = next(get_session())
        service = RecipeService(session)
        deleted = service.delete_recipe(recipe_id)
        session.close()
        return deleted


schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(max_depth=10),
    ]
)
graphql_router = GraphQLRouter(schema)
