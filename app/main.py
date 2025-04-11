from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_table
from app.router import tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(tables.router, prefix='/tables', tags=['Tables'])
@app.get('/')
def root():
    return {'message': 'API is running!'}
