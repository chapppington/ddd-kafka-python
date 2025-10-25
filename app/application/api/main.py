from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler
from punq import Container

from application.api import main_router
from application.api.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)
from logic.init import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)
    job = await scheduler.spawn(consume_in_background())

    yield

    await close_message_broker()
    await job.close()


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
