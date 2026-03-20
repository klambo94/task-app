import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


env = os.getenv("APP_ENV", "local")  # defaults to local

# Load the correct .env file before pydantic-settings reads anything
env_files = {
    "test": ".env.test",
    "local": ".env.local",
    "dev": ".env.dev",
    "prod": ".env.prod"
}
print(f"[settings] APP_ENV={env}, loading {env_files[env]}")

load_dotenv(env_files[env])

class Settings(BaseSettings):
    environment: str = env
    database_url: str
    alembic_url: str
    nextauth_secret: str
    frontend_url: str


    @property
    def is_testing(self) -> bool:
        return self.environment == "test"

ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
NEXTAUTH_SECRET = os.getenv("NEXTAUTH_SECRET")
FRONT_END_URL = os.getenv("FRONT_END_URL")

settings = Settings(alembic_url=ALEMBIC_DATABASE_URL,
                    database_url=DATABASE_URL,
                    nextauth_secret=NEXTAUTH_SECRET,
                    frontend_url=FRONT_END_URL)