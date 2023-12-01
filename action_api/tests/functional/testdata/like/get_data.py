import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
ITEM_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)

LIKE_GET_DATA = [
    (
        {"timestamp": 10000, "payload": {"item_type": "review", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 20000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 30000, "payload": {"item_type": "review", "rating": 10}},
        ITEM_ID,
        JWT_TOKEN,
    ),
]

LIKE_GET_NO_DATA = [
    (
        uuid.uuid4(),
        JWT_TOKEN,
    ),
]

LIKE_GET_INVALID = [
    (
        {"timestamp": 10000, "payload": {"item_type": "review", "rating": 5}},
        "invalid_uuid",
        JWT_TOKEN,
    ),
    (
        {"timestamp": 20000, "payload": {"item_type": "movie", "rating": 5}},
        "invalid_uuid",
        JWT_TOKEN,
    ),
    (
        {"timestamp": 30000, "payload": {"item_type": "review", "rating": 10}},
        "invalid_uuid",
        JWT_TOKEN,
    ),
]

LIKE_GET_RATING_DATA = [
    (
        [
            {
                "timestamp": 10000,
                "payload": {
                    "item_type": "movie",
                    "rating": 10,
                },
                "jwt_token": utils_tokens.create_correct_token(uuid.uuid4()),
            }
            for _ in range(50)
        ]
        + [
            {
                "timestamp": 20000,
                "payload": {
                    "item_type": "movie",
                    "rating": 5,
                },
                "jwt_token": utils_tokens.create_correct_token(uuid.uuid4()),
            }
            for _ in range(50)
        ],
        {"timestamp": 10000, "payload": {"item_type": "movie"}},
        7.5,
        uuid.UUID("66666666-6666-6666-6666-666666666666"),
        JWT_TOKEN,
    ),
    (
        [
            {
                "timestamp": 10000,
                "payload": {
                    "item_type": "review",
                    "rating": 7,
                },
                "jwt_token": utils_tokens.create_correct_token(uuid.uuid4()),
            }
            for _ in range(50)
        ]
        + [
            {
                "timestamp": 20000,
                "payload": {
                    "item_type": "review",
                    "rating": 3,
                },
                "jwt_token": utils_tokens.create_correct_token(uuid.uuid4()),
            }
            for _ in range(50)
        ],
        {"timestamp": 20000, "payload": {"item_type": "review"}},
        50,
        uuid.UUID("77777777-7777-7777-7777-777777777777"),
        JWT_TOKEN,
    ),
]


LIKE_GET_RATING_INVALID = [
    (
        {"timestamp": 10000, "payload": {"item_type": "movie"}},
        7.5,
        "invalid_uuid",
        JWT_TOKEN,
    ),
]
