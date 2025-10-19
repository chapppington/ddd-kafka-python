from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.websocket("{chat_oid}")
async def messages_handlers(chat_oid: str, websocket: WebSocket):
    await websocket.accept()
