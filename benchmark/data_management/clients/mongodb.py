import uuid

import pymongo
from core.config import settings
from data_management import clickstream_chunk_generator
from data_management.clients.base_client import BaseDBClient
from shemas.entity import Event


class MongoClient(BaseDBClient):
    def __init__(self):
        self.client: pymongo.MongoClient = None
        self.db_name = settings.mongo.db_name
        self.db_table = settings.mongo.collection_name

    def _flatten_query(self, query_dict, parent_key="", sep="."):
        """
        Преобразует вложенный словарь в плоский словарь, используя точку как разделитель для ключей.
        """
        items = {}
        for k, v in query_dict.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_query(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def connect(self, **kwargs) -> pymongo.MongoClient:
        self.client: pymongo.MongoClient = pymongo.MongoClient(
            f"mongodb://{settings.mongo.user}:{settings.mongo.password}@"
            f"{settings.mongo.host}:{settings.mongo.port}/?authMechanism=DEFAULT",
            uuidRepresentation="standard",
        )
        return self.client

    def disconnect(self):
        self.client.close()

    def create_db(self):
        # Будет создана при добавлении данных
        pass

    def create_table(self):
        if settings.mongo.use_index:
            self.client[self.db_name][self.db_table].create_index(
                [("user_id", 1), ("event_type", 1)]
            )
            self.client[self.db_name][self.db_table].create_index(
                [("user_id", 1), ("event_data.like_type", 1)]
            )
            self.client[self.db_name][self.db_table].create_index(
                [("movie_id", 1), ("event_type", 1), ("event_data.rating", 1)]
            )

    def drop_database(self):
        self.client.drop_database(self.db_name)

    @BaseDBClient.timing_decorator
    def load_data(self, limit: int):
        total_load = 0
        while total_load < limit:
            payloads: list[Event] = clickstream_chunk_generator.get_payloads()
            events = [event.model_dump() for event in payloads]
            self.client[self.db_name][self.db_table].insert_many(events)
            total_load += len(payloads)

    @BaseDBClient.timing_decorator
    def update_data(self, ids: list[uuid.UUID] = None, updates: dict = None):
        if not ids or len(ids) == 0:
            return 0
        if updates is None:
            updates = {}

        # Преобразование фильтров и обновлений в формат, понимаемый MongoDB
        mongo_filters = {"_id": {"$in": ids}}
        mongo_updates = {"$set": self._flatten_query(updates)}

        result = self.client[self.db_name][self.db_table].update_many(
            mongo_filters,
            mongo_updates,
            upsert=False,
        )
        return result.modified_count

    @BaseDBClient.timing_decorator
    def select_data(
        self, filters: dict = None, attrs: list = None, queries_limit: int = 0
    ):
        if filters is None:
            filters = {}
        if attrs is None:
            attrs = {}
        else:
            attrs = {field: 1 for field in attrs}

        mongo_query = self._flatten_query(filters)
        result = list(
            self.client[self.db_name][self.db_table]
            .find(mongo_query, attrs)
            .limit(queries_limit)
        )

        return result

    def clear_table(self):
        return self.client[self.db_name][self.db_table].delete_many({})

    @BaseDBClient.timing_decorator
    def get_count(self):
        return self.client[self.db_name][self.db_table].count_documents({})

    def get_database_size(self):
        stats = self.client[self.db_name].command("dbStats")
        size = stats.get("dataSize") / (1024 * 1024)  # В мегабайтах
        return round(size, 2)
