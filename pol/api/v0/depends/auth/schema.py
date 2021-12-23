from typing import Optional

from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request
from fastapi.security.http import SecurityBase
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.utils import get_authorization_scheme_param

from pol import res


class OptionalHTTPBearer(SecurityBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        description: Optional[str] = (
            "You don't need a access token to access this API "
            "but you may not access some private or sensitive resource."
        ),
        scheme_name: Optional[str] = None,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return ""
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (scheme and credentials):
            raise res.HTTPException(
                title="unauthorized",
                status_code=HTTP_403_FORBIDDEN,
                description="Not authenticated",
            )
        if scheme.lower() != "bearer":
            raise res.HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                title="unauthorized",
                description="Invalid authentication credentials",
            )
        return credentials


class HTTPBearer(SecurityBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        description: Optional[str] = (
            "You can create a personal access token at "
            "[https://bgm.tv/dev/app](https://bgm.tv/dev/app)"
        ),
        scheme_name: Optional[str] = None,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        exc = res.HTTPException(
            title="unauthorized",
            status_code=HTTP_403_FORBIDDEN,
            description="Not authenticated",
        )
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise exc
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (scheme and credentials):
            raise exc
        if scheme.lower() != "bearer":
            raise res.HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                title="unauthorized",
                description="Invalid authentication credentials",
            )
        return credentials
