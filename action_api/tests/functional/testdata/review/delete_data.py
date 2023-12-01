import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
MOVIE_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)


REVIEW_DELETE_DATA = [
    (
        {"timestamp": 10000, "payload": {"text": "Отличный фильм!"}},
        MOVIE_ID,
        JWT_TOKEN,
    ),
    (
        {"timestamp": 20000, "payload": {"text": "Отличный фильм!"}},
        uuid.uuid4(),
        JWT_TOKEN,
    ),
]

REVIEW_DELETE_NO_DATA = [
    (
        MOVIE_ID,
        JWT_TOKEN,
    ),
]

REVIEW_DELETE_INVALID = [
    (
        {"timestamp": 10000, "payload": {"text": "Отличный фильм!"}},
        "invalid_id",
        JWT_TOKEN,
    ),
]
