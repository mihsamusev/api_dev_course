from app import models, oauth2, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_vote(
    vote_data: schemas.VoteCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote_data.post_id).first()
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"post with id: {vote_data.post_id} was not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == user.id, models.Vote.post_id == post.id
    )
    vote = vote_query.first()
    if not vote:
        if vote_data.is_up:
            new_vote = models.Vote(post_id=post.id, user_id=user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "vote added successfully"}
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"No vote from user {user.id} to remove from post {post.id}",
            )
    elif vote:
        if not vote_data.is_up:
            vote_query.delete()
            db.commit()
            return {"message": "vote deleted successfully"}
        else:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"User {user.id} has already voted on post {post.id}",
            )
