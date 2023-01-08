# noqa: ANN401
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, TypeVar, Union, overload

K = TypeVar("K")
V = TypeVar("V")


class BaseConfig(dict, ABC):
    def __init__(self, path: str) -> None:
        self._path = path

        self.config = self.load(path)

    @abstractmethod
    def load(self, path: str) -> dict[str, Any]:  # Must be a dictionary
        ...

    # Export the config to a JSON file
    @abstractmethod
    def to_json(self) -> None:
        ...

    # Get a config value using `.get` and can be casted to a type, and can have a default value
    @overload
    def get(
        self, key: str, cast: None = None, default: Optional[V] = None
    ) -> Union[str, V]:
        ...

    @overload
    def get(
        self, key: str, cast: Callable[[str], K], default: Optional[V] = None
    ) -> Union[K, V]:
        ...

    def get(
        self, key: str, cast: Optional[Callable[[str], Any]] = None, default: Any = None
    ) -> Any:
        if not cast:
            cast = lambda x: x

        # Raise error when not found and no default value
        if not default:
            value = self.config[key]
        else:
            value = self.config.get(key, default)

        return cast(value)

    def __getattr__(self, name: str) -> object:
        try:
            return self.config[name]
        except KeyError:
            raise AttributeError(f"Config has no attribute '{name}'")

    def __setattr__(self, key: str, value: object) -> None:
        super().__setattr__(key, value)

    def __setitem__(self, key: str, value: object) -> None:
        super().__setitem__(key, value)

    def __delattr__(self, value: str) -> None:
        super().__delitem__(value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self._path})"


class BaseConfigLoader(ABC):
    def __init__(self, path: str) -> None:
        self._path = path
        self.config = self.load(path)

    @abstractmethod
    def load(self, path: str) -> dict[str, Any]:  # Must be a dictionary
        ...

    @abstractmethod
    def to_json(self, config: Any) -> None:
        ...

    # Reload the config - can be triggered on file change
    def reload(self) -> None:
        self.config = self.load(self._path)

    # Get any properties using `config.property_name`
    def __getattr__(self, name: str) -> Any:
        try:
            return self.config[name]
        except KeyError:
            raise AttributeError(f"Config has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"
