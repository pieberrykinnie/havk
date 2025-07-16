from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_session
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceRead
from .deps import get_current_user

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=List[ResourceRead])
async def list_resources(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Resource))
    return result.all()


@router.post("/", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    *,
    resource_in: ResourceCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    resource = Resource(**resource_in.dict())
    session.add(resource)
    await session.commit()
    await session.refresh(resource)
    return resource