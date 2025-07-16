from pydantic import BaseModel


class SolutionBase(BaseModel):
    title: str
    description: str | None = None
    resource_id: int


class SolutionCreate(SolutionBase):
    pass


class SolutionRead(SolutionBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True