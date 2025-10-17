from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ChatException(ApplicationException):
    @property
    def message(self) -> str:
        return "Chat exception occurred"


@dataclass(eq=False)
class TitleTooLongException(ChatException):
    text: str

    @property
    def message(self) -> str:
        return f"Title too long: {self.text[:30]}..."


@dataclass(eq=False)
class EmptyTitleException(ChatException):
    @property
    def message(self) -> str:
        return "Title is empty"
