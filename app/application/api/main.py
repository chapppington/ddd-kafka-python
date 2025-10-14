from fastapi import FastAPI

from application.api import main_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Kafka Python",
        description="DDD Kafka Python",
        docs_url="/api/docs",
        debug=True,
    )

    app.include_router(main_router)

    return app
