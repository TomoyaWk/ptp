from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ptp_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    PROJECT_NAME: str = "PTP"
    API_V1_STR: str = "/api"


settings = Settings()
