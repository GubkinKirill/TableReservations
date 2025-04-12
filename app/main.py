from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_table
from app.router import tables
from app.router import reservations

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(tables.router, prefix='/tables', tags=['Tables'])
app.include_router(reservations.router, prefix='/reservations', tags=['Reservations'])
@app.get('/')
def root():
    return {'message': 'API is running!'}
