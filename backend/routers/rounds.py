from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import get_current_user
from models import CreateRound, UpdateRound, User

router = APIRouter(prefix="/rounds", tags=["rounds"])


@router.get("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_rounds(_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_round(
    _body: CreateRound,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{round_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_round(
    _round_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.patch("/{round_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_round(
    _round_id: UUID,
    _body: UpdateRound,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.delete("/{round_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_round(
    _round_id: UUID,
    _user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
