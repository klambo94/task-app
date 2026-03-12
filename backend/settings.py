from dotenv import load_dotenv
import os


env = os.getenv("APP_ENV", "local")  # defaults to local

env_files = {
    "test": ".env.test",
    "local": ".env.local",
    "dev": ".env.dev",
    "prod": ".env.prod"
}
print(f"[settings] APP_ENV={env}, loading {env_files[env]}")

load_dotenv(env_files[env])

POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
POSTGRES_DB : str = os.getenv("POSTGRES_DB","psinaptic_db")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
FRONT_END_URL : str = os.getenv("FRONT_END_URL","http://localhost:3000")

INTERNAL_SECRET = os.getenv("INTERNAL_API_SECRET")
