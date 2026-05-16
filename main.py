from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import init_db, periodic_sync
from routes.payments import router as payments_router
from routes.webhooks import router as webhooks_router
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    print("DB initialized")
    asyncio.create_task(periodic_sync(interval= 60))

    yield

    # shutdown (если понадобится)
    print("App stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(payments_router)
app.include_router(webhooks_router)

@app.get("/ping")
async def ping():
    return {"status": "payments ok"}