from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "sidekick_db"
    HF_TOKEN: str = "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" 

    class Config:
        env_file = ".env"

config = Settings()