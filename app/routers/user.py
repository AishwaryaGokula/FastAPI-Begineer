from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import get_db

router = APIRouter( prefix="/users",tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.userResponse)
def create_user(user:schemas.users,db: Session = Depends(get_db)):
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.users(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
@router.get("/{id}",response_model=schemas.userResponse)
def get_users(id:int,db: Session = Depends(get_db)):
    past_user = db.query(models.users).filter(models.users.id ==id).first()
    if not past_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {id} is not found . please try with correct id")
    return past_user