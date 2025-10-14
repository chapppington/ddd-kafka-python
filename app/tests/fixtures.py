from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.messages import (
    BaseChatRepository,
    DummyInMemoryChatRepository,
)
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()

    container.register(
        BaseChatRepository,
        DummyInMemoryChatRepository,
        scope=Scope.singleton,
    )

    return container
