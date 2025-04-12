from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

def has_conflict(db: Session, new_reservation: ReservationCreate) -> bool:
    new_start = new_reservation.reservation_time
    new_end = new_start + timedelta(minutes=new_reservation.duration_minutes)

    existing_reservations = db.query(Reservation).filter(
        Reservation.table_id == new_reservation.table_id
    ).all()

    for res in existing_reservations:
        res_start = res.reservation_time
        res_end = res_start + timedelta(minutes=res.duration_minutes)
        if new_start < res_end and new_end > res_start:
            return True

    return False
