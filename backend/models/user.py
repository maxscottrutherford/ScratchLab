from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    email: str
    full_name: str | None = None
    handicap_index: Decimal | None = None
    created_at: datetime


class UpdateUser(BaseModel):
    full_name: str | None = None
    handicap_index: Decimal | None = None
