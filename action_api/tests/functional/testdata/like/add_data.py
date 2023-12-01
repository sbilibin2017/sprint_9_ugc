import http
import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
ITEM_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)

LIKE_ADD_DATA = [
    (
        {"timestamp": 10000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 20000, "payload": {"item_type": "review", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 30000, "payload": {"item_type": "movie", "rating": 0}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 40000, "payload": {"item_type": "review", "rating": 0}},
        ITEM_ID,
        JWT_TOKEN,
    ),
]

LIKE_ADD_INVALID_BODY = [
    (
        {"timestamp": 10000, "payload": {"rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {
            "timestamp": 30000,
            "payload": {
                "item_type": "movie",
            },
        },
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"payload": {"item_type": "review", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 50000, "payload": {"item_type": "not_item", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 60000, "payload": {"item_type": "review", "rating": -1}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 70000, "payload": {"item_type": "review", "rating": 11}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 80000, "payload": {"item_type": "review", "rating": 0}},
        "invalid_uuid",
        JWT_TOKEN,
    ),
]

LIKE_INVALID_TOKEN = [
    (
        {"timestamp": 10000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        BAD_TOKENS[1],
        http.HTTPStatus.UNAUTHORIZED,
    ),
    (
        {"timestamp": 20000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        BAD_TOKENS[2],
        http.HTTPStatus.UNAUTHORIZED,
    ),
    (
        {"timestamp": 30000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        BAD_TOKENS[3],
        http.HTTPStatus.UNAUTHORIZED,
    ),
    (
        {"timestamp": 40000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        BAD_TOKENS[4],
        http.HTTPStatus.UNAUTHORIZED,
    ),
]
