from infrastructure.repositories.messages import BaseChatRepository
from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
) -> Mediator:
    mediator.register_command(
        command=CreateChatCommand,
        command_handlers=[
            CreateChatCommandHandler(chat_repository=chat_repository),
        ],
    )
