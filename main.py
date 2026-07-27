from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from loguru import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def startup_event():
    logger.info('Starting backend application')

app.include_router(api_router, prefix='/api')

@app.get('/')
def root():
    return {'message': 'University Student Assistant backend is running'}
