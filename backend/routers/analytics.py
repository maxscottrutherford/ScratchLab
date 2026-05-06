from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import get_current_user
from models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/strokes-gained/{round_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def strokes_gained_for_round(
    _round_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/trends", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def trends(_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/handicap", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def handicap_analytics(_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
