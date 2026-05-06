from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

CourseSource = Literal["api", "manual"]


class Course(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    name: str
    location: str | None = None
    par: int
    slope_rating: Decimal | None = None
    course_rating: Decimal | None = None
    source: CourseSource | None = None
    external_id: str | None = None
    created_by: UUID | None = None
    created_at: datetime


class CreateCourse(BaseModel):
    name: str
    location: str | None = None
    par: int
    slope_rating: Decimal | None = None
    course_rating: Decimal | None = None
    source: CourseSource | None = "manual"
    external_id: str | None = None
