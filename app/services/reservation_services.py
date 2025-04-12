from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate   

def has_conflict(db: Session, new_reservation: ReservationCreate) -> bool:
    new_start = new_reservation.reservation_time
    new_end = new_start + timedelta(minutes=new_reservation.duration_minutes)

    overlapping = db.query(Reservation).filter(
        Reservation.table_id == new_reservation.table_id,
        Reservation.reservation_time < new_end,
        (Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes)) > new_start
    ).first()
    return overlapping is not None