import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
MOVIE_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)

BOOKMARK_ADD_DATA = [
    (
        uuid.uuid4(),
        JWT_TOKEN,
    ),
    (
        MOVIE_ID,
        JWT_TOKEN,
    ),
    (
        MOVIE_ID,
        JWT_TOKEN,
    ),
]

BOOKMARK_ADD_INVALID = [
    (
        "invalid_id",
        JWT_TOKEN,
    ),
]
