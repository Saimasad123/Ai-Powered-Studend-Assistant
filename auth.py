from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.services.auth_service import create_access_token, verify_password, get_password_hash
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


@router.post('/register', response_model=UserRead)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token(str(user.id))
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
