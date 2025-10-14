from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from domain.entities.messages import ChatEntity


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    def add_chat(self, chat: ChatEntity): ...


@dataclass
class DummyInMemoryChatRepository(BaseChatRepository):
    _saved_chats: list[ChatEntity] = field(default_factory=list, kw_only=True)

    def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return (
                next(chat for chat in self._saved_chats if chat.title.value == title)
                is not None
            )
        except StopIteration:
            return False

    def add_chat(self, chat: ChatEntity):
        self._saved_chats.append(chat)
