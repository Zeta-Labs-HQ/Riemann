from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Mapping, Type

Row = Mapping[str, Any]


class BaseDatabase(ABC):
    __slots__ = ("connection", "is_closed")

    def __init__(self, connection: object) -> None:
        self.connection = connection
        self.is_closed = False

    @abstractmethod
    async def close(self) -> None:
        if self.is_closed:
            return

    @abstractmethod
    async def __aenter__(self) -> object:
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        pass


class Connection(ABC):
    @abstractmethod
    async def execute(self, query: str, *args: Any) -> None:
        ...

    @abstractmethod
    async def execute_many(self, query: str, args: Any) -> None:
        ...

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> Row:
        ...

    @abstractmethod
    async def fetch_many(self, query: str, *args: Any) -> list[Row]:
        ...

    @abstractmethod
    async def fetch_all(self, query: str, *args: Any) -> list[Row]:
        ...

    @abstractmethod
    async def fetch_one(self, query: str, *args: Any) -> Row:
        ...
