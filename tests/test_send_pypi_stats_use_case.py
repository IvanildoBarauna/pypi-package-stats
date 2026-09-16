from types import SimpleNamespace

import pandas as pd
import pytest

from src.domain.use_cases import send_metrics_use_case


class FakeTracer:
    pass


class FakeDataWarehouse:
    def __init__(self):
        self.updated_batches = []

    def update_downloads(self, downloads_list, project_name):
        self.updated_batches.append((downloads_list, project_name))
        return "updated", None


class FakeMetricsService:
    def __init__(self, result=("sent", None)):
        self.result = result
        self.calls = []

    def send(self, tags, value, timestamp):
        self.calls.append((tags, value, timestamp))
        return self.result


def make_use_case(monkeypatch, metrics_result=("sent", None)):
    warehouse = FakeDataWarehouse()
    metrics = FakeMetricsService(metrics_result)

    monkeypatch.setattr(send_metrics_use_case, "DWService", lambda: warehouse)
    monkeypatch.setattr(send_metrics_use_case, "SendMetricsService", lambda: metrics)
    monkeypatch.setattr(
        send_metrics_use_case,
        "tracing_service",
        SimpleNamespace(get_tracer=lambda: FakeTracer()),
    )

    return send_metrics_use_case.SendPypiStatsUseCase(), warehouse, metrics


def make_dataframe(rows):
    return pd.DataFrame(
        [
            {
                "DOWNLOAD_ID": index,
                "DTTM": 1_700_000_000 + index,
                "COUNTRY_CODE": "BR",
                "PROJECT": "example-project",
                "PACKAGE_VERSION": "1.0.0",
                "INSTALLER_NAME": "pip",
                "PYTHON_VERSION": "3.11",
            }
            for index in range(rows)
        ]
    )


def test_send_stats_skips_empty_dataframe(monkeypatch):
    use_case, warehouse, metrics = make_use_case(monkeypatch)

    use_case.send_stats(make_dataframe(0))

    assert metrics.calls == []
    assert warehouse.updated_batches == []


def test_send_stats_sends_tags_and_flushes_partial_batch(monkeypatch):
    use_case, warehouse, metrics = make_use_case(monkeypatch)

    use_case.send_stats(make_dataframe(2))

    assert metrics.calls == [
        (
            [
                "country_code:BR",
                "project:example-project",
                "package_version:1.0.0",
                "installer_name:pip",
                "python_version:3.11",
            ],
            1,
            1_700_000_000,
        ),
        (
            [
                "country_code:BR",
                "project:example-project",
                "package_version:1.0.0",
                "installer_name:pip",
                "python_version:3.11",
            ],
            1,
            1_700_000_001,
        ),
    ]
    assert warehouse.updated_batches == [([0, 1], "example-project")]


def test_send_stats_flushes_each_hundred_downloads(monkeypatch):
    use_case, warehouse, metrics = make_use_case(monkeypatch)

    use_case.send_stats(make_dataframe(101))

    assert len(metrics.calls) == 101
    assert warehouse.updated_batches == [
        (list(range(100)), "example-project"),
        ([100], "example-project"),
    ]


def test_send_stats_raises_when_metrics_submission_fails(monkeypatch):
    use_case, warehouse, _ = make_use_case(monkeypatch, metrics_result=("", "denied"))

    with pytest.raises(Exception, match="denied"):
        use_case.send_stats(make_dataframe(1))

    assert warehouse.updated_batches == []
