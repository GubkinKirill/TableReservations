from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_services import has_conflict

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[ReservationRead])
def get_all_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@router.post('/', response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    if has_conflict(db, reservation):
        raise HTTPException(status_code=409, detail="Table is already reserved for this time slot")

    new_res = Reservation(**reservation.model_dump())
    db.add(new_res)
    db.commit()
    db.refresh(new_res)
    return new_res

@router.delete('/{reservation_id}', response_model=None)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(res)
    db.commit()
    return {'message': 'Reservation deleted successfully'}
