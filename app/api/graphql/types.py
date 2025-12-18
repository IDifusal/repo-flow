import strawberry
from datetime import datetime


@strawberry.type
class RecipeType:
    id: int
    title: str
    description: str | None
    created_at: datetime
