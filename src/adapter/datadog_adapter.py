from datetime import datetime
from typing import Tuple, Optional
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries
from src.application.ports.metrics_interface import MetricsPort
from src.application.use_cases.get_secrets import GetSecretValueUseCase


class DataDogAPIAdapter(MetricsPort):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.secret_manager = GetSecretValueUseCase()
        self.configuration = Configuration()
        self.configuration.api_key["apiKeyAuth"] = self._get_dd_api_key()
        self.configuration.host = self._get_dd_host()
        self.configuration.debug = False
        self.configuration.enable_retry = True
        self.configuration.max_retries = 3

    def _get_dd_api_key(self):
        return self.secret_manager.get(secret_id="datadog-pypi-package-stats")

    def _get_dd_host(self):
        return self.secret_manager.get(secret_id="datadog-host")

    def increment(self, tags: list, value: int, timestamp) -> Tuple[str, Optional[str]]:
        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=self.metric_name,
                    type=MetricIntakeType.COUNT,
                    points=[
                        MetricPoint(
                            # """ Add historical timestamp here """
                            timestamp=int(timestamp),
                            # """ *********************** """
                            value=value,
                        ),
                    ],
                    tags=tags,
                ),
            ],
        )

        try:
            with ApiClient(self.configuration) as api_client:
                api_instance = MetricsApi(api_client)
                response = api_instance.submit_metrics(body=body)
        except Exception as e:
            return "", str(e)

        if response.to_dict()["errors"]:
            return "", response.to_str()

        print("Sended metrics with body: ", body)
        return response.to_str()
