from fastapi import APIRouter

from application.api.chats.handlers import router as chats_router


main_router = APIRouter()

main_router.include_router(chats_router)
