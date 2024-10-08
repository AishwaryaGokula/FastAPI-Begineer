from fastapi import FastAPI,Depends,Response,status,HTTPException,APIRouter
from .. import schemas,utils,models,OAuth2
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(prefix = "/login", tags=['Authentication'])

@router.post("",response_model=schemas.Token)
def user_login(user_login: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    # Checking Email Address or Username is valid or not
    user = db.query(models.users).filter(models.users.email == user_login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    # Checking if password is valid or not - 
    if not utils.verify_user(user_login.password,user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    access_token = OAuth2.create_access_token(data= {"user_id":user.id})
    return {"access_token" : access_token, "token_type":"Bearer"}

# When client sends the username and password - there will be validation - after validation is cleared, access token is returned
# Access token is returned to client


    



 