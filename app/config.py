from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    container and validation for environmental variables
    """

    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
