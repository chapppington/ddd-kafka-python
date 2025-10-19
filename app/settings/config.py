from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_chat_database: str = Field(default="chat", alias="MONGODB_CHAT_DATABASE")
    mongodb_chat_collection: str = Field(
        default="chat",
        alias="MONGODB_CHAT_COLLECTION",
    )
    mongodb_message_collection: str = Field(
        default="message",
        alias="MONGODB_MESSAGE_COLLECTION",
    )
    new_message_received_topic: str = Field(default="new-message-received-topic")
    new_chats_event_topic: str = Field(default="new-chats-topic")
    kafka_url: str = Field(alias="KAFKA_URL")

    # без этого не будут подставляться значения из .env файла
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
