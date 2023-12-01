import uuid

import tests.functional.utils.tokens as utils_tokens

USER_UUID = uuid.uuid4()
MOVIE_ID = uuid.uuid4()
JWT_TOKEN = utils_tokens.create_correct_token(USER_UUID)
BAD_TOKENS = utils_tokens.create_all_bad_tokens(USER_UUID)

BOOKMARK_GET_DATA = [
    (
        uuid.uuid4(),
        JWT_TOKEN,
    ),
]

BOOKMARK_GET_NO_DATA = [
    (
        uuid.uuid4(),
        JWT_TOKEN,
    ),
]

BOOKMARK_GET_INVALID = [
    (
        "invalid_uuid",
        JWT_TOKEN,
    ),
]
