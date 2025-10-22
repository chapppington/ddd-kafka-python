from fastapi import APIRouter

from application.api.chats.handlers import router as chats_router
from application.api.chats.websockets.messages import router as messages_ws_router


main_router = APIRouter()

main_router.include_router(chats_router)
main_router.include_router(messages_ws_router)
