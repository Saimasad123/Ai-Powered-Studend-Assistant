from sqlalchemy import JSON
from sqlalchemy.sql.schema import Column
from app.core.config import settings

try:
    from pgvector.sqlalchemy import Vector
except ImportError:  # pragma: no cover
    Vector = None


def get_embedding_column_type():
    if 'postgres' in settings.DATABASE_URL and Vector is not None:
        return Vector(1536)
    return JSON
