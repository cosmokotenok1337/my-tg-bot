from pydantic import BaseModel, Field


class BotServiceModel(BaseModel):
    """Bot service schema"""

    title: str = Field(max_length=50)
    description: str
    user_id: int
