from src.application.ports.datawarehouse_interface import DataWarehousePort
from typing import Type


class DWService:
    def __init__(self, datawarehouse: Type[DataWarehousePort]):
        self.datawarehouse = datawarehouse

    def query_execute(self, query: str):
        return self.datawarehouse.query_execute(query)

    def query_to_dataframe(self, query: str):
        return self.datawarehouse.query_to_dataframe(query)
