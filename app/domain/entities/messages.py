from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.messages import TextValueObject


@dataclass(eq=False)
class MessageEntity(BaseEntity):
    text: TextValueObject
