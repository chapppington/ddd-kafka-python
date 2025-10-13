from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class MessageException(ApplicationException):
    @property
    def message(self) -> str:
        return "Message exception occurred"


@dataclass(eq=False)
class EmptyTextException(MessageException):
    @property
    def message(self) -> str:
        return "Text is empty"


@dataclass(eq=False)
class TitleTooLongException(MessageException):
    text: str

    @property
    def message(self) -> str:
        return f"Title too long: {self.text[:30]}..."
