from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from middleware.auth import get_current_user
from models import CreateCourse, User

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/search", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def search_courses(
    _q: str | None = Query(default=None),
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_course(
    _body: CreateCourse,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{course_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_course(
    _course_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
