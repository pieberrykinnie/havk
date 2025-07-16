from typing import Optional

from sqlmodel import Field, SQLModel


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: str | None = None
    category: str | None = None