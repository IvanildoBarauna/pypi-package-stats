from typing import Tuple, Optional
from google.cloud import secretmanager
from src.application.ports.secret_manager_interface import ISecretManager


class SecretManagerAdapter(ISecretManager):
    """
    A class used to represent a SecretManagerAdapter
    """

    def __init__(self) -> None:
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def get_secret_value(self, secret_id: str) -> Tuple[Optional[str], str]:
        request = {
            "name": f"projects/ivanildobarauna/secrets/{secret_id}/versions/latest",
        }

        try:
            secret_request = self.secret_client.access_secret_version(request=request)
        except ValueError as e:
            return str(e), ""

        return None, secret_request.payload.data.decode("UTF-8")
