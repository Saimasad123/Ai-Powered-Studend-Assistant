from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.models.user import User

router = APIRouter()


@router.get('/', response_model=list[CourseRead])
def list_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.user_id == current_user.id).all()


@router.post('/', response_model=CourseRead)
def create_course(course_create: CourseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = Course(user_id=current_user.id, **course_create.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_or_404(course_id: int, user_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@router.get('/{course_id}', response_model=CourseRead)
def read_course(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_course_or_404(course_id, current_user.id, db)


@router.put('/{course_id}', response_model=CourseRead)
def update_course(course_id: int, course_update: CourseUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = get_course_or_404(course_id, current_user.id, db)
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(course, field, value)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.delete('/{course_id}')
def delete_course(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = get_course_or_404(course_id, current_user.id, db)
    db.delete(course)
    db.commit()
    return {'detail': 'Course deleted'}
