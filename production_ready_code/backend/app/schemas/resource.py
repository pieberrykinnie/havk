from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int

    class Config:
        orm_mode = True