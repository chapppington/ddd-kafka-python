from dataclasses import dataclass

from domain.exceptions.messages import (
    EmptyTextException,
    TextTooLongException,
    TitleTooLongException,
)
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class TextValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise TextTooLongException(text=self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class TitleValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 50:
            raise TitleTooLongException(text=self.value)

    def as_generic_type(self):
        return str(self.value)
