from pydantic_settings import BaseSettings
from pydantic import ConfigDict
class Settings(BaseSettings):
    
    db_driver:str = "postgresql"
    db_username:str
    db_password:str
    db_host:str
    db_port:str
    db_database:str

    model_config = ConfigDict(env_file = ".env")

settings = Settings()

