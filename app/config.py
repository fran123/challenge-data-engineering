from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    db_driver:str = "postgresql"
    db_username:str
    db_password:str
    db_host:str
    db_port:str
    db_database:str

    class Config:
        env_file = ".env"


settings = Settings()

