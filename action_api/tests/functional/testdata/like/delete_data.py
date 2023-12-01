import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
ITEM_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)


LIKE_DELETE_DATA = [
    (
        {"timestamp": 10000, "payload": {"item_type": "movie", "rating": 5}},
        ITEM_ID,
        JWT_TOKEN,
    ),
]

LIKE_DELETE_NO_DATA = [
    (
        uuid.uuid4(),
        JWT_TOKEN,
    ),
]

LIKE_DELETE_INVALID = [
    (
        {"timestamp": 10000, "payload": {"item_type": "movie", "rating": 5}},
        "invalid_uuid",
        JWT_TOKEN,
    ),
]
