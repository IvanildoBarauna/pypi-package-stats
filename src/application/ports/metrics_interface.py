# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod


class MetricsPort(ABC):
    def __init__(self, metric_name: str):
        pass

    @abstractmethod
    def increment(
        self,
        tags: list,
        value: int,
        timestamp: float,
    ) -> None:
        pass
