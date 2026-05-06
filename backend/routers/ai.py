from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import get_current_user
from models import User

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/transcribe", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def transcribe(_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/extract-hole", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def extract_hole(_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
