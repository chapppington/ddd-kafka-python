from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Kafka Python",
        description="DDD Kafka Python",
        docs_url="/api/docs",
        debug=True,
    )

    return app
