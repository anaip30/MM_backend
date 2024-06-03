
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  

class Settings(BaseSettings):
    database_url: str = "mongodb://localhost:2717/defaultdb"

settings = Settings()
