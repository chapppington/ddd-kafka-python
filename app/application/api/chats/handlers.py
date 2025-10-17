from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from application.api.chats.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
)
from application.api.schemas import ErrorResponseSchema
from domain.exceptions.base import ApplicationException
from logic.commands.chats import CreateChatCommand
from logic.init import init_container
from logic.mediator import Mediator


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создаёт новый чат, если чат с таким названием существует, то возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container=Depends(init_container),
):
    """Создать новый чат."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateChatResponseSchema.from_entity(chat)
