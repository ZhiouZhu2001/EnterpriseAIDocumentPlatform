import redis
from pathlib import Path
import psycopg
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str
    db_port: int
    db_user: str
    db_password: SecretStr
    db_name: str
    redis_host: str
    redis_port: int

settings = Settings()
app = FastAPI()

@app.get("/live")
def check_health_live():
    return {"status": "ok", "message": "API is running."}


@app.get("/ready")
def check_health_ready_pg():
    try:
        with psycopg.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password.get_secret_value(),
            dbname=settings.db_name,
            connect_timeout=2,
            options="-c statement_timeout=2000",
        ) as connection:
            connection.execute("SELECT 1").fetchone()
    except psycopg.Error as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    try:
        r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, socket_connect_timeout=2)
        r.ping()
    except redis.exceptions.RedisError as exc:
        raise HTTPException(status_code=503, detail="Redis is unavailable") from exc

    return {"status": "ok", "message": "Database is ready."}
