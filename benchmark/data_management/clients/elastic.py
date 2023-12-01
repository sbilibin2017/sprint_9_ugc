import json
import uuid

from core.config import settings
from data_management import clickstream_chunk_generator
from data_management.clients.base_client import BaseDBClient
from elasticsearch import Elasticsearch, helpers
from shemas.entity import Event


class ElasticsearchClient(BaseDBClient):
    def __init__(self):
        self.client: Elasticsearch = None
        self.index_name = settings.elastic.index_name

    @staticmethod
    def _transform_event_for_es(event):
        data = event.model_dump()
        # Преобразовываем UUIDs в строки
        data["user_id"] = str(data["user_id"])
        data["movie_id"] = str(data["movie_id"])

        return data

    @staticmethod
    def _construct_term_queries(filters: dict):
        queries = []
        for key, value in filters.items():
            if isinstance(value, dict):
                for inner_key, inner_value in value.items():
                    queries.append({"term": {f"{key}.{inner_key}": inner_value}})
            else:
                queries.append({"term": {f"{key}": value}})
        return queries

    def connect(self, **kwargs) -> Elasticsearch:
        self.client = Elasticsearch(
            f"http://{settings.elastic.host}:{settings.elastic.port}"
        )
        return self.client

    def disconnect(self):
        del self.client

    def create_db(self):
        with open("data_management/shema_design.json") as file:
            mappings = json.load(file)

        if self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)

        self.client.indices.create(index=self.index_name, body=mappings)

    def create_table(self):
        pass

    def drop_database(self):
        self.client.indices.delete(index=self.index_name)

    @BaseDBClient.timing_decorator
    def load_data(self, limit: int):
        total_load = 0
        while total_load < limit:
            payloads: list[Event] = clickstream_chunk_generator.get_payloads()
            events = [
                {
                    "_index": self.index_name,
                    "_source": self._transform_event_for_es(event),
                }
                for event in payloads
            ]

            helpers.bulk(self.client, events)
            total_load += len(payloads)

    @BaseDBClient.timing_decorator
    def update_data(self, ids: list[uuid.UUID] = None, updates: dict = None):
        if not ids or len(ids) == 0:
            return 0
        if updates is None:
            updates = {}

        actions = [
            {
                "_op_type": "update",
                "_index": self.index_name,
                "_id": str(id_),
                "doc": updates,
            }
            for id_ in ids
        ]
        response = helpers.bulk(self.client, actions)
        return response[0]

    @BaseDBClient.timing_decorator
    def select_data(
        self, filters: dict = None, attrs: list = None, queries_limit: int = 0
    ):
        if filters is None:
            filters = {}
        attrs = attrs if attrs is not None else []

        must_queries = self._construct_term_queries(filters)

        query = {"size": 1000, "query": {"bool": {"must": must_queries}}}
        if queries_limit:
            query["size"] = queries_limit

        if attrs:
            query["_source"] = attrs

        results = self.client.search(index=self.index_name, body=query)
        if attrs:
            return [
                {
                    attr: hit.get(attr, None)
                    if attr == "_id"
                    else hit["_source"].get(attr, None)
                    for attr in attrs
                }
                for hit in results["hits"]["hits"]
            ]

        else:
            return [
                {"_id": hit["_id"], **hit["_source"]} for hit in results["hits"]["hits"]
            ]

    def clear_table(self):
        # Просто удаляем и создаем индекс заново
        self.drop_database()
        self.create_db()

    @BaseDBClient.timing_decorator
    def get_count(self):
        return self.client.count(index=self.index_name)["count"]

    def get_database_size(self):
        stats = self.client.indices.stats(index=self.index_name)
        size = stats["indices"][self.index_name]["total"]["store"]["size_in_bytes"] / (
            1024 * 1024
        )  # В мегабайтах
        return round(size, 2)
