"""This module describes routes for basic API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, posts, users, vote

# create tables with SQLAlchemy if they are not already there
# models.Base.metadata.create_all(bind=engine)
# we use alembic instead

app = FastAPI(
    title="Social Network",
    description=open("README.md", "r", encoding="UTF").read(),
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mihhail Samusev",
        "url": "http://example.com/",
        "email": "mih.samusev@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# setup CORS policy
origins = ["*"]  # public API, or narrow down to list of domains

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "i changed, a lot"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
