from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
)
from application.api.schemas import ErrorResponseSchema
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatAlreadyExistsException
from logic.init import init_container
from logic.mediator import Mediator


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create a new chat",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateChatResponseSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponseSchema,
        },
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container=Depends(init_container),
):
    """Create a new chat."""
    mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ChatAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail={"error": exception.message})

    return CreateChatResponseSchema.from_entity(chat)
