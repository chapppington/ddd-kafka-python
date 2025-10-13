from dataclasses import dataclass
from domain.value_objects.base import BaseValueObject
from domain.exceptions.messages import MessageTooLongException

@dataclass(frozen=True)
class TextValueObject(BaseValueObject):

    value: str
    
    def validate(self):
        if len(self.value) >255:
            raise MessageTooLongException(text=self.value)
    
    def as_generic_type(self):
        return str(self.value)