import os
from pathlib import Path
from dotenv import load_dotenv


# =========================================================
# BASE DIRECTORY
# =========================================================

base_dir = Path(__file__).resolve().parent.parent.parent

# Load backend/.env
load_dotenv(base_dir / ".env")


# =========================================================
# DATABASE URL
# =========================================================

def normalize_sqlite_url(database_url: str) -> str:

    if database_url.startswith("sqlite:///"):

        db_path = Path(
            database_url.replace(
                "sqlite:///",
                ""
            )
        )

        if not db_path.is_absolute():

            db_path = (
                base_dir
                / db_path
            ).resolve()

        db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        return f"sqlite:///{db_path}"

    return database_url


# =========================================================
# SETTINGS
# =========================================================

class Settings:

    # -----------------------------------------------------
    # Application
    # -----------------------------------------------------

    PROJECT_NAME: str = os.getenv(
        "APP_NAME",
        "University Student Assistant"
    )


    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------

    DATABASE_URL: str = normalize_sqlite_url(
        os.getenv(
            "DATABASE_URL",
            "sqlite:///./backend/storage/app.db"
        )
    )


    # -----------------------------------------------------
    # JWT Authentication
    # -----------------------------------------------------

    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "change-me"
    )

    JWT_ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "120"
        )
    )


    # -----------------------------------------------------
    # File Uploads
    # -----------------------------------------------------

    UPLOAD_DIRECTORY: str = os.getenv(
        "UPLOAD_DIRECTORY",
        str(
            base_dir
            / "storage"
            / "uploads"
        )
    )

    MAX_UPLOAD_SIZE_MB: int = int(
        os.getenv(
            "MAX_UPLOAD_SIZE_MB",
            "20"
        )
    )


    # =====================================================
    # GROQ AI
    # =====================================================

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )


    # -----------------------------------------------------
    # RAG
    # -----------------------------------------------------

    VECTOR_TOP_K: int = int(
        os.getenv(
            "VECTOR_TOP_K",
            "5"
        )
    )


    # -----------------------------------------------------
    # Logging
    # -----------------------------------------------------

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )


# =========================================================
# CREATE SETTINGS INSTANCE
# =========================================================

settings = Settings()


# =========================================================
# CREATE STORAGE DIRECTORIES
# =========================================================

storage_dir = (
    Path(
        settings.UPLOAD_DIRECTORY
    )
    .resolve()
    .parent
)

storage_dir.mkdir(
    parents=True,
    exist_ok=True
)

Path(
    settings.UPLOAD_DIRECTORY
).resolve().mkdir(
    parents=True,
    exist_ok=True
)