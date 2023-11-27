from abc import ABC, abstractmethod

from ORM.schemas import SMarkIn


class BaseFilter(ABC):
    def __init__(self, sort_key: str, sort_value: str):
        self.sort_key = sort_key
        self.sort_value = sort_value

    @abstractmethod
    def __call__(self, schema: SMarkIn) -> bool:
        ...


class TwoAllFilter(BaseFilter):
    def __call__(self, schema: SMarkIn):
        return all((
            str(schema.mark) == "2",
            self.sort_value is True,
        ))


class NotTwoAllFilter(BaseFilter):
    def __call__(self, schema: SMarkIn):
        return all((
            str(schema.mark) in ("3", "4", "5"),
            self.sort_value is True,
        ))


class TwoMatchAttrFilter(BaseFilter):
    def __call__(self, schema: SMarkIn):
        return all((
            getattr(schema, self.sort_key, None) == self.sort_value,
            str(schema.mark) == "2",
        ))


class NotTwoMatchAttrFilter(BaseFilter):
    def __call__(self, schema: SMarkIn):
        return all((
            getattr(schema, self.sort_key, None) == self.sort_value,
            str(schema.mark) in ("3", "4", "5"),
        ))
