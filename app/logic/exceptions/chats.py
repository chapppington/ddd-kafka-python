from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self) -> str:
        return f"Chat with title '{self.title}' already exists"


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_oid: str

    @property
    def message(self) -> str:
        return f"Chat with oid '{self.chat_oid}' not found"
