from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

Lie = Literal["tee", "fairway", "rough", "sand", "green", "penalty", "unknown"]


class Shot(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    round_hole_id: UUID
    shot_number: int
    club: str | None = None
    distance_yards: int | None = None
    lie_before: Lie | None = None
    lie_after: Lie | None = None
    strokes_gained: Decimal | None = None
    created_at: datetime


class CreateShot(BaseModel):
    shot_number: int
    club: str | None = None
    distance_yards: int | None = None
    lie_before: Lie | None = None
    lie_after: Lie | None = None
    strokes_gained: Decimal | None = None
