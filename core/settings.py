from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    token_duration: int
    algorithm: str
    
    debug: bool = False


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()