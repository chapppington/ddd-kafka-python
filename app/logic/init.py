from functools import lru_cache

from aiokafka.producer import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from domain.events.chats import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.repositories.chats.base import BaseChatsRepository
from infrastructure.repositories.chats.mongo import MongoDBChatsRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.repositories.messages.mongo import MongoDBMessagesRepository
from logic.commands.chats import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from logic.commands.messages import (
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.events.chats import NewChatCreatedEventHandler
from logic.events.messages import NewMessageReceivedEventHandler
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.chats import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
)
from logic.queries.messages import (
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_chats_mongodb_repository() -> BaseChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_database_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_messages_mongodb_repository() -> BaseMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_database_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_message_collection,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chats_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton,
    )

    # Command handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
        )

    # Message Broker
    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chats_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            messages_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository),
        )
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )

        new_message_received_handler = NewMessageReceivedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.new_message_received_topic,
        )

        mediator.register_event(
            NewChatCreatedEvent,
            [new_chat_created_event_handler],
        )

        mediator.register_event(
            NewMessageReceivedEvent,
            [new_message_received_handler],
        )

        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )

        # Register query handlers
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
