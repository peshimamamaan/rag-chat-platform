from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    GEMINI_API_KEY: str 
    NANGO_SECRET_KEY: str
    NANGO_HOST: str

    class Config:
        env_file = ".env"

settings = Settings()