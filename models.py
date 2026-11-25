from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=200)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = False

    