from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Solution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    resource_id: int = Field(foreign_key="resource.id")
    creator_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)