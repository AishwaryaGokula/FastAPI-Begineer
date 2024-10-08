from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models,schemas,OAuth2
from ..database import get_db


router = APIRouter(prefix="/votes",tags=['Votes'])

router.post("/",status_code=status.HTTP_201_CREATED)
def votes(votes:schemas.Votes,db:Session=Depends(get_db),current_user: int=Depends(OAuth2.get_current_user)):
    def votes(votes: schemas.Votes, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
        if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
        
        vote_query = db.query(models.votes).filter(models.votes.post_id == votes.post_id, models.votes.user_id == current_user.id)
        found_vote = vote_query.first()
        if votes.dir == 1:
           if found_vote:
        # If the vote exists, remove it (toggle action)
            db.delete(found_vote)
            db.commit()
            return {"message": "Successfully removed the vote"}
           else:
                new_vote = models.votes(post_id=votes.post_id, user_id=current_user.id)
                db.add(new_vote)
                db.commit()
                return {"message": "Successfully added the vote"}
        elif votes.dir == -1:
            if found_vote:
        # If a vote exists (either upvote or downvote), remove it
             db.delete(found_vote)
             db.commit()
            return {"message": "Successfully removed the vote"}
          
        
            
            
            
           

           
        
 
   
        
        
        

            
              
       
        

    


  
    

         


           

        
        
    

      
    

   

    