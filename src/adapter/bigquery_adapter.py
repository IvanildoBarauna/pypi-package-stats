from google.cloud import bigquery
from pandas.core.frame import DataFrame
from typing import Type, Optional, Tuple
from src.application.ports.datawarehouse_interface import DataWarehousePort


class BigQueryAdapter(DataWarehousePort):
    """
    A class used to represent a BigQueryAdapter

    """

    def __init__(self):
        self.bigquery_conn = bigquery.Client()

    def query_execute(self, query: str) -> Tuple[bigquery.QueryJob, Optional[str]]:
        """
        Get data from BigQuery
        """
        # Perform a query.
        _query = query
        query_job = self.bigquery_conn.query(_query)

        if query_job.errors:
            return query_job, str(query_job.error_result)

        return query_job, None

    def query_to_dataframe(self, query: str) -> Tuple[DataFrame, Optional[str]]:
        _query = query
        query_job = self.bigquery_conn.query(_query)

        df = DataFrame()

        if query_job.errors:
            return df, str(query_job.error_result)

        df = query_job.to_dataframe()

        return df
