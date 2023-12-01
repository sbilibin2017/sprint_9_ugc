import hashlib
import json
import uuid
from datetime import datetime

import tests.config as tests_config
from jose import jwt


def _uuid_with_zeroed_part(id_str: str):
    return id_str[0:9] + "0000" + id_str[13:]


def hash_user_agent(user_agent: str):
    """
    Функция для хеширования строки User-Agent. Возвращает хеш-строку.

    :param user_agent: Строка User-Agent для хеширования
    :return: SHA256 хеш от входной строки
    """
    return hashlib.sha256(user_agent.encode()).hexdigest()


def create_token(
    identity: uuid.UUID | str,
    expiration_time: int,
    key: str | None = None,
    scopes: list[str] | None = None,
) -> str:
    secret_key = tests_config.tests_settings.jwt_secret_key
    data = str(identity)
    claims = {"sub": data, "exp": expiration_time}
    if scopes:
        claims["scopes"] = json.dumps(scopes)
    return jwt.encode(
        claims,
        key=(key or secret_key),
        algorithm=tests_config.tests_settings.jwt_algorithm,
        headers={"alg": "HS256", "typ": "JWT"},
    )


def create_token_with_access(
    identity: uuid.UUID, permissions: list[str] | None = None
) -> str:
    if permissions is None:
        permissions = []
    current_time = int(datetime.now().timestamp())
    issue_time = current_time - 15
    expiration_time = issue_time + 300
    return create_token(identity, expiration_time, scopes=permissions)


def create_correct_token(
    identity: uuid.UUID,
    permissions: list[str] | None = None,
) -> str:
    if permissions is None:
        permissions = []
    current_time = int(datetime.now().timestamp())
    issue_time = current_time - 15
    expiration_time = issue_time + 300
    return create_token(identity, expiration_time, scopes=permissions)


def create_token_for_missing_user(
    identity: uuid.UUID,
    permissions: list[str] | None = None,
) -> str:
    if permissions is None:
        permissions = []
    sub = _uuid_with_zeroed_part(str(identity))
    current_time = int(datetime.now().timestamp())
    issue_time = current_time - 15
    expiration_time = issue_time + 300
    return create_token(sub, expiration_time, scopes=permissions)


def create_expired_token(
    identity: uuid.UUID,
    permissions: list[str] | None = None,
) -> str:
    if permissions is None:
        permissions = []
    current_time = int(datetime.now().timestamp())
    issue_time = current_time - 300
    expiration_time = issue_time + 150
    return create_token(identity, expiration_time, scopes=permissions)


def create_token_with_wrong_key(
    identity: uuid.UUID,
    permissions: list[str] | None = None,
) -> str:
    if permissions is None:
        permissions = []
    current_time = int(datetime.now().timestamp())
    issue_time = current_time - 15
    expiration_time = issue_time + 300
    secret_key = tests_config.tests_settings.jwt_secret_key
    return create_token(
        identity,
        expiration_time,
        "not_" + secret_key,
        scopes=permissions,
    )


def create_all_bad_tokens(
    identity: uuid.UUID,
) -> list[str | None]:
    return [
        create_token_for_missing_user(identity),
        create_expired_token(identity),
        create_token_with_wrong_key(identity),
        "non-existing-token",
        None,
    ]
