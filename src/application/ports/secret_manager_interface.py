# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ISecretManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_secret_value(self, secret_id: str) -> Tuple[Optional[str], str]:
        pass
