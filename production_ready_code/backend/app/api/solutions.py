from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..models.solution import Solution
from ..schemas.solution import SolutionCreate, SolutionRead
from .deps import get_current_user

router = APIRouter(prefix="/solutions", tags=["solutions"])


@router.get("/", response_model=List[SolutionRead])
async def list_solutions(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Solution))
    return result.all()


@router.post("/", response_model=SolutionRead, status_code=status.HTTP_201_CREATED)
async def create_solution(
    *,
    solution_in: SolutionCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    solution = Solution(**solution_in.dict(), creator_id=user.id)
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution