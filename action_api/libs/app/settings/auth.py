import pydantic
import pydantic_settings


class AuthSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    jwt_secret_key: str = pydantic.Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = pydantic.Field("HS256", alias="TOKEN_SIGN_ALGORITHM")
