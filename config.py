import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  

class Settings(BaseSettings):
    database_url: str = os.getenv("DB_URL", "mongodb://localhost:27017/defaultdb")

settings = Settings()
