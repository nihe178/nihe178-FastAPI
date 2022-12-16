from .. import models, schemas, oauth2, database
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} was not found.")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted for this post.")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)    
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added your vote."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your vote for this post connot been found.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted your vote."}