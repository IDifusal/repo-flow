from datetime import datetime
from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class RecipeRead(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
