from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

TeesPlayed = Literal["black", "blue", "white", "red"]


class Round(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    user_id: UUID
    course_id: UUID
    played_at: date
    tees_played: TeesPlayed | None = None
    total_score: int | None = None
    total_putts: int | None = None
    fairways_hit: int | None = None
    greens_in_regulation: int | None = None
    handicap_differential: Decimal | None = None
    is_complete: bool = False
    synced_at: datetime | None = None
    created_at: datetime


class CreateRound(BaseModel):
    course_id: UUID
    played_at: date
    tees_played: TeesPlayed | None = None


class UpdateRound(BaseModel):
    played_at: date | None = None
    tees_played: TeesPlayed | None = None
    total_score: int | None = None
    total_putts: int | None = None
    fairways_hit: int | None = None
    greens_in_regulation: int | None = None
    handicap_differential: Decimal | None = None
    is_complete: bool | None = None
    synced_at: datetime | None = None
