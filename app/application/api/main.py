from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api import main_router
from application.api.lifespan import (
    close_message_broker,
    init_message_broker,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    yield
    await close_message_broker()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Kafka Python",
        description="DDD Kafka Python",
        docs_url="/api/docs",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(main_router)

    return app
