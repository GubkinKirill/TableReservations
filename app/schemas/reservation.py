from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

class ReservationRead(ReservationCreate):
    id: int

    model_config ={'from_attributes': True}