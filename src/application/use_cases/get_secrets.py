from src.application.services.get_secret_value_service import GetSecretValueService
from src.adapter.secret_manager_adapter import SecretManagerAdapter


class GetSecretValueUseCase:
    """
    A class used to represent a GetSecretValueUseCase
    """

    def __init__(self) -> None:
        self.secretmanager = SecretManagerAdapter()
        self.get_secret_value_service = GetSecretValueService(
            secret_manager=self.secretmanager
        )

    def get(self, secret_id: str) -> str:
        """
        Get secret value
        """
        err, secret_value = self.get_secret_value_service.get(secret_id=secret_id)

        if err:
            raise Exception(err)

        return secret_value
