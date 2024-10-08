from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


# Base Model - used for validation of fields - models (django)
# Base Model is derived from pydantic library

class users(BaseModel):
    email : EmailStr
    password : str

    class Config:
        from_attributes = True


class Post(BaseModel):
    title : str
    content : str
    published : bool = True

    class Config:
        from_attributes = True


class CreatePost(Post):
    pass

class userResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

class ResponsePost(BaseModel):
    title : str
    content : str
    published : bool 
    owner_id : int
    owner : userResponse

    class Config:
        from_attributes = True
        



class user_login(BaseModel):
    email : EmailStr
    password : str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None


class Votes(BaseModel):
    post_id : int
    
    