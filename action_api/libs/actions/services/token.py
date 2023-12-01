import fastapi
import fastapi.security as fastapi_security
import jose
import jose.jwt as jose_jwt
import libs.actions.models as actions_models
import libs.app.config as app_config
import pydantic

oauth2_scheme = fastapi_security.OAuth2PasswordBearer(tokenUrl="token")


def get_token_data(token: str = fastapi.Depends(oauth2_scheme)):
    try:
        secret_key = app_config.auth_settings.jwt_secret_key
        payload = jose_jwt.decode(
            token, secret_key, algorithms=[app_config.auth_settings.jwt_algorithm]
        )
        return actions_models.TokenResponseModel(**payload)
    except (jose.JWTError, pydantic.ValidationError):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
