from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.table import Table
from app.schemas.table import TableCreate, TableRead
from fastapi.responses import JSONResponse


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[TableRead])
def get_all_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.post('/', response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    new_table = Table(**table.model_dump())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.delete('/{table_id}', response_class=JSONResponse)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"message": "Table deleted successfully"}

