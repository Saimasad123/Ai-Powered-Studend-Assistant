import os
from pathlib import Path

os.environ.setdefault('DATABASE_URL', 'sqlite:///./backend/storage/test.db')

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine
from app.db.base import Base

Path('./backend/storage').mkdir(parents=True, exist_ok=True)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)
