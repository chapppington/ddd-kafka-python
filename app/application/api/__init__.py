from fastapi import APIRouter

from application.api.messages.handlers import router as messages_router


main_router = APIRouter()

main_router.include_router(messages_router)
