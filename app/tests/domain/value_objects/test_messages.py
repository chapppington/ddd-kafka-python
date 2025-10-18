from datetime import datetime

import pytest

from domain.entities.chats import ChatEntity
from domain.entities.messages import MessageEntity
from domain.events.chats import NewMessageReceivedEvent
from domain.exceptions.chats import TitleTooLongException
from domain.exceptions.messages import TextTooLongException
from domain.value_objects.chats import TitleValueObject
from domain.value_objects.messages import TextValueObject


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
        # Create a chat to get a valid chat_oid
        title = TitleValueObject(value="Test Chat")
        chat = ChatEntity(title=title)
        message = MessageEntity(chat_oid=chat.oid, text=text)
        assert message.text == text
        assert message.chat_oid == chat.oid
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

    message = MessageEntity(
        chat_oid=chat.oid,
        text=TextValueObject(value="Hello, world!"),
    )

    chat.add_message(message)

    assert message in chat.messages
    assert message.chat_oid == chat.oid
    assert chat.created_at.date() == datetime.today().date()
    assert chat.updated_at.date() == datetime.today().date()


def test_new_message_received_event():
    title = TitleValueObject(value="Hello, world!")
    chat = ChatEntity(title=title)
    message = MessageEntity(
        chat_oid=chat.oid,
        text=TextValueObject(value="Hello, world!"),
    )
    chat.add_message(message)

    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
