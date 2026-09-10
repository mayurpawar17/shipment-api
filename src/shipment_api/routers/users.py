from fastapi import APIRouter, HTTPException, Depends,status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserResponse
from ..database import get_db
from ..models import User


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Convert validated request data into an ORM object, persist it, and reload
    # it so generated values such as the primary-key ID are available.
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve a user by ID. If not found, raise a 404 error.
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Pagination prevents this endpoint from loading every user at once.
    return db.query(User).offset(skip).limit(limit).all()   