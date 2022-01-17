from typing import List, Optional

from app import models, oauth2, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostVotedResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    result = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return result


@router.get("/my", response_model=List[schemas.PostResponse])
def get_my_posts(
    db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)
):
    """
    Only users posts
    """
    result = db.query(models.Post).filter(models.Post.owner_id == user.id).all()
    return result


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id: {id} was not found"
        )
    return result


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    new_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    result = db.query(models.Post).filter(models.Post.id == id)
    post = result.first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id: {id} was not found"
        )

    if post.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")

    result.update(new_post.dict())
    db.commit()
    return post


@router.delete("/{id}", tags=["posts"])
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    result = db.query(models.Post).filter(models.Post.id == id)
    post = result.first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id: {id} was not found"
        )

    if post.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")
    result.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
