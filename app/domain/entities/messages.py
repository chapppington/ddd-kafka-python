from dataclasses import dataclass, field
import uuid
from datetime import datetime
from domain.value_objects.messages import TextValueObject


@dataclass
class MessageEntity:
    oid: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: TextValueObject
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
