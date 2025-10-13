from dataclasses import dataclass 
from datetime import datetime
from domain.value_objects.messages import TextValueObject

@dataclass
class MessageEntity:
    oid: str
    text: TextValueObject
    created_at: datetime
    updated_at: datetime