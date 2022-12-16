from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_SVR_URL: str
    POSTGRES_SVR_PRT: str
    POSTGRES_SVR_USR: str
    POSTGRES_SVR_PWD: str
    POSTGRES_SVR_DB: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRY_TIME: int

    class Config:
        env_file = ".env"

settings = Settings()