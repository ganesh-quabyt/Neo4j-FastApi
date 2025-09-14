from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
