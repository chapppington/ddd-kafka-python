from dataclasses import dataclass
from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class MessageException(ApplicationException):
    @property
    def message(self) -> str:
        return "Message exception occurred"


@dataclass(eq=False)
class MessageTooLongException(MessageException):
    
    text: str
    
    @property
    def message(self) -> str:
        return f"Message too long (>255 characters): {self.text[:30]}..."
