import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

import redis.asyncio as redis

# Для запуска "вне Docker" по умолчанию localhost.
# В Compose эти переменные придут из .env и будут ссылаться на db/redis.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://app:app@localhost:5432/appdb")
REDIS_URL    = os.getenv("REDIS_URL",    "redis://localhost:6379/0")

class EchoIn(BaseModel):
    value: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
    r = redis.from_url(REDIS_URL, decode_responses=True)

    # Создадим простую таблицу и проверим Redis
    async with engine.begin() as conn:
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pings (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
    await r.ping()

    app.state.engine = engine
    app.state.redis = r
    try:
        yield
    finally:
        await app.state.redis.aclose()
        await app.state.engine.dispose()

app = FastAPI(title="FastAPI + Postgres + Redis", lifespan=lifespan)

@app.get("/health")
async def health():
    async with app.state.engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    await app.state.redis.ping()
    return {"ok": True}

@app.get("/db-ping")
async def db_ping():
    async with app.state.engine.begin() as conn:
        await conn.execute(text("INSERT INTO pings DEFAULT VALUES"))
        row = await conn.execute(text("SELECT COUNT(*) FROM pings"))
        total = row.scalar_one()
    return {"ok": True, "rows_in_pings": total, "ts": datetime.now(timezone.utc).isoformat()}

@app.post("/cache/echo")
async def cache_echo(inp: EchoIn):
    await app.state.redis.set("last_echo", inp.value, ex=60)
    return {"saved": inp.value}

@app.get("/cache/echo")
async def cache_echo_get():
    return {"last_echo": await app.state.redis.get("last_echo")}
