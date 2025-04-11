from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return {'message': 'API is running!'}
