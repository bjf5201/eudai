from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv(dotenv_path=".env.server")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    APP_NAME: str = "EUDAI"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = ""

    class Config:
        env_file = ".env.server"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
