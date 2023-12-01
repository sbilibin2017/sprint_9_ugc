import logging
import random

from core.config import settings
from data_management import base_data
from shemas.entity import LikeType


def data_filling(client, limit: int):
    load_time = client.load_data(limit)
    count_docs = client.get_count()
    return load_time.execute_time, count_docs.execute_result


def research_algorithm(client):
    user_like_query = {
        "user_id": random.choice(base_data.users),
        "event_data": {"like_type": LikeType.LIKE.value},
    }
    result = client.select_data(user_like_query)
    logging.info(
        f"Like search. Time - {result.execute_time}s. Find documents - {len(result.execute_result)}."
    )

    movie_like_query = {
        "movie_id": random.choice(base_data.movies),
        "event_type": "Like",
        "event_data": {"like_type": LikeType.LIKE.value},
    }
    result = client.select_data(movie_like_query, attrs=["_id"])
    logging.info(
        f"Movie like search. Time - {result.execute_time}s. Find documents - {len(result.execute_result)}."
    )

    movie_like_query = {
        "movie_id": random.choice(base_data.movies),
        "event_type": "Like",
        "event_data": {"like_type": LikeType.DISLIKE.value},
    }
    result = client.select_data(movie_like_query, attrs=["_id"])
    logging.info(
        f"Movie dislike search. Time - {result.execute_time}s. Find documents - {len(result.execute_result)}."
    )

    middle_rating = {
        "movie_id": random.choice(base_data.movies),
        "event_type": "Rating",
    }

    result = client.select_data(middle_rating, attrs=["rating"])
    logging.info(
        f"Middle rating search. Time - {result.execute_time}s. Find documents - {len(result.execute_result)}."
    )

    update_criteria = {
        "movie_id": random.choice(base_data.movies),
        "event_type": "Rating",
    }
    update_new_values = {"event_data": {"rating": random.randint(0, 10)}}
    result = client.select_data(
        update_criteria, attrs=["_id"], queries_limit=settings.update_limit
    )
    update_ids = [x["_id"] for x in result.execute_result]

    # Массово обновляем
    result = client.update_data(ids=update_ids, updates=update_new_values)
    logging.info(
        f"Rating update for multiple documents. Time - {result.execute_time}s. "
        f"Documents updated - {result.execute_result}."
    )
