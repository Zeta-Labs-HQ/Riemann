import logging
from abc import ABC, abstractmethod


# Needs attention: Won't the subclass be async for discord logging in order to send messages?
class BaseLogger(ABC):
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self._name = name
        self._level = level

    @abstractmethod
    def log(self, message: str, level: int = logging.INFO) -> None:
        ...

    def debug(self, message: str) -> None:
        self.log(message, logging.DEBUG)

    def info(self, message: str) -> None:
        self.log(message, logging.INFO)

    def warning(self, message: str) -> None:
        self.log(message, logging.WARNING)

    def error(self, message: str) -> None:
        self.log(message, logging.ERROR)

    def critical(self, message: str) -> None:
        self.log(message, logging.CRITICAL)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name}, level={self._level})"
