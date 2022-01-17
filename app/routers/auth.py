from app import models, oauth2, schemas, utils
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=["authentication"])


@router.post("/", response_model=schemas.Token)
def login_user(
    login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    # check user exists
    user = db.query(models.User).filter(models.User.email == login.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid credentials")

    correct_pass = utils.verify(login.password, user.password)

    if not correct_pass:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid credentials")
    # generate token
    access_token = oauth2.create_access_token(payload={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
