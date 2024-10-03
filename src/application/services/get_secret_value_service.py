from typing import Type, Tuple, Optional
from src.application.ports.secret_manager_interface import ISecretManager


class GetSecretValueService:
    """
    A class used to represent a GetSecretValueService
    """

    def __init__(self, secret_manager: Type[ISecretManager]):
        """
        Constructor method for GetSecretValueService
        """
        self.manager = secret_manager

    def get(self, secret_id: str) -> Tuple[Optional[str], str]:
        """
        Get secret value
        """
        err, secret_value = self.manager.get_secret_value(secret_id=secret_id)

        if err:
            return (
                f"[GetSecretValueService.get]: error getting secret value -> {err}",
                "",
            )

        return None, secret_value
