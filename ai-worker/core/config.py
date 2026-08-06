from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    lmstudio_base_url: str = "http://localhost:1234/v1"
    lmstudio_api_key: str = "lm-studio"
    lmstudio_model: str = "meta-llama-3.1-8b-instruct"
    tavily_api_key: str = ""
    database_url: str = "sqlite:///database.db"
    verify_ssl: bool = False
    telegram_bot_token: str = ""
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_QUEUE: str = "research_tasks"

    class Config:
        env_file = "../.env"
        extra = "ignore"

settings = Settings()