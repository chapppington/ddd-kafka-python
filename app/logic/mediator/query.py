from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QueryResultType,
    QueryType,
)


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: dict[QueryType, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(
        self,
        query: QueryType,
        query_handler: BaseQueryHandler[QueryType, QueryResultType],
    ) -> QueryResultType: ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QueryResultType: ...
