from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import get_current_user
from models import CreateRoundHole, User

router = APIRouter(prefix="/rounds", tags=["holes"])


@router.post("/{round_id}/holes", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_round_hole(
    _round_id: UUID,
    _body: CreateRoundHole,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{round_id}/holes", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_round_holes(
    _round_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.patch("/{round_id}/holes/{hole_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_round_hole(
    _round_id: UUID,
    _hole_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
