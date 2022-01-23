import pytest
from app.config import settings
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}_test".format(
    settings.db_username,
    settings.db_password,
    settings.db_hostname,
    settings.db_port,
    settings.db_name,
)

db_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


if __name__ == "__main__":
    pass
