import random
import warnings

from core.config import settings
from data_management import base_data
from shemas.entity import Bookmark, Event, Like, Rating, Review

warnings.filterwarnings("ignore")


class PayloadGenerator:
    def __init__(self, chunk_size: int = settings.CHUNK_SIZE):
        self.movie_ids = base_data.movies
        self.user_ids = base_data.users
        self.chunk_size = chunk_size
        self.EVENT_TYPES = [Bookmark, Like, Rating, Review]

    def _generate_event(self):
        user_id = random.choice(self.user_ids)
        movie_id = random.choice(self.movie_ids)
        event_data = random.choice(self.EVENT_TYPES)()
        event_type = event_data.__class__.__name__

        return Event(
            user_id=user_id,
            movie_id=movie_id,
            event_type=event_type,
            event_data=event_data,
        )

    def get_all_generated_events(self):
        return [self._generate_event() for _ in range(self.chunk_size)]


def get_payloads():
    payload_generator = PayloadGenerator()
    return payload_generator.get_all_generated_events()
