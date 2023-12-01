import abc
import time
import uuid
from functools import wraps

from shemas.entity import QueryTimeResult


class BaseDBClient(abc.ABC):
    def timing_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            return QueryTimeResult(
                execute_time=format(end_time - start_time, ".2f"), execute_result=result
            )

        return wrapper

    @abc.abstractmethod
    def connect(self, **kwargs):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def create_db(self, **kwargs):
        pass

    @abc.abstractmethod
    def create_table(self, **kwargs):
        pass

    @abc.abstractmethod
    def drop_database(self):
        pass

    @abc.abstractmethod
    def load_data(self, limit: int, chunk_size: int):
        pass

    @abc.abstractmethod
    def select_data(self, filters: dict, attrs: list):
        pass

    @abc.abstractmethod
    def update_data(self, ids: list[uuid.UUID] = None, updates: dict = None):
        pass

    @abc.abstractmethod
    def clear_table(self):
        pass

    @abc.abstractmethod
    def get_count(self, **kwargs):
        pass

    def get_database_size(self):
        pass
