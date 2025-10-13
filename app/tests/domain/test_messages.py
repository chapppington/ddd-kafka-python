from datetime import datetime

import pytest

from domain.entities.messages import (
    ChatEntity,
    MessageEntity,
)
from domain.exceptions.messages import (
    TextTooLongException,
    TitleTooLongException,
)
from domain.value_objects.messages import (
    TextValueObject,
    TitleValueObject,
)


@pytest.mark.parametrize(
    "text_value,should_raise",
    [
        ("Hello, world!", False),  # short text, should succeed
        ("A" * 256, True),  # long text, should raise
    ],
)
def test_create_message(text_value, should_raise):
    if should_raise:
        with pytest.raises(TextTooLongException):
            TextValueObject(value=text_value)
    else:
        text = TextValueObject(value=text_value)
        message = MessageEntity(text=text)
        assert message.text == text
        assert message.created_at.date() == datetime.today().date()


@pytest.mark.parametrize(
    "title_value,should_raise",
    [
        ("Hello, world!", False),  # short title, should succeed
        ("A" * 51, True),  # long title, should raise
    ],
)
def test_create_chat(title_value, should_raise):
    if should_raise:
        with pytest.raises(TitleTooLongException):
            TitleValueObject(value=title_value)
    else:
        title = TitleValueObject(value=title_value)
        chat = ChatEntity(title=title)

        assert chat.title == title
        assert chat.created_at.date() == datetime.today().date()


def test_add_message_to_chat():
    title = TitleValueObject(value="Hello, world!")
    chat = ChatEntity(title=title)
    message = MessageEntity(text=TextValueObject(value="Hello, world!"))
    chat.add_message(message)
    assert message in chat.messages
    assert chat.created_at.date() == datetime.today().date()
    assert chat.updated_at.date() == datetime.today().date()
