from typing import Tuple, Optional, Type
from src.application.ports.metrics_interface import MetricsPort


class SendMetricsService:
    def __init__(self, MetricsRepository: Type[MetricsPort]):
        self.metrics_repository = MetricsRepository

    def send(
        self,
        tags: list,
        value: int,
        timestamp: float,
    ) -> Tuple[str, Optional[str]]:
        return self.metrics_repository.increment(
            tags=tags, value=value, timestamp=timestamp
        )
