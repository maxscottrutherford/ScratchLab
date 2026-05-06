from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Hole(BaseModel):
    """Course hole (layout) — `public.holes`."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    course_id: UUID
    hole_number: int
    par: int
    yardage_black: int | None = None
    yardage_blue: int | None = None
    yardage_white: int | None = None
    yardage_red: int | None = None


class RoundHole(BaseModel):
    """Per-round hole scoring — `public.round_holes`."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    round_id: UUID
    hole_id: UUID
    hole_number: int
    par: int
    score: int | None = None
    putts: int | None = None
    fairway_hit: bool | None = None
    green_in_regulation: bool | None = None
    raw_description: str | None = None
    created_at: datetime


class CreateRoundHole(BaseModel):
    hole_id: UUID
    hole_number: int
    par: int
    score: int | None = None
    putts: int | None = None
    fairway_hit: bool | None = None
    green_in_regulation: bool | None = None
    raw_description: str | None = None
