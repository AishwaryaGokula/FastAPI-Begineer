from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models,schemas,OAuth2
from ..database import get_db


router = APIRouter(prefix="/posts",tags=['Posts'])


@router.get("/",response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(OAuth2.get_current_user),limit : int = 10,skip : int = 0,search:Optional[str]="" ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # Fetch all posts from the database
    return posts


@router.get("/{id}",response_model=schemas.ResponsePost)
def get_post_id(id:int,db: Session = Depends(get_db),current_user : int = Depends(OAuth2.get_current_user)):
    #  cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    #  existing_post = cursor.fetchone()
     req_post = db.query(models.Post).filter(models.Post.id == id).first()
     if not req_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} is not present")
     return req_post
     
     

@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_posts(post : schemas.CreatePost, db: Session = Depends(get_db),current_user : int = Depends(OAuth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
  
    new_post = models.Post(**post.__dict__,owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user : int = Depends(OAuth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id) # Providing the sql query 
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post of {id} is not present")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the requested action ")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.ResponsePost)
def update_post(id:int, post:schemas.CreatePost,db: Session = Depends(get_db),current_user : int = Depends(OAuth2.get_current_user)):
    updated_query = db.query(models.Post).filter(models.Post.id == id)
    retrieved_post = updated_query.first()
    if retrieved_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post of {id} is not present")
    updated_post =updated_query.update(post.model_dump(),synchronize_session=False)
    if retrieved_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the requested action ")
    db.commit()
    db.refresh(retrieved_post)
    return retrieved_post
