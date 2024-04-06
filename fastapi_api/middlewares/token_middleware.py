from time import perf_counter
from configs import Config
from starlette import status
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthHeaderMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        if str(getattr(getattr(request, "url", None), "path", None)) not in Config.INSECURE_PATHS:
            if check_if_token_is_not_valid(request=request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session geçerli değil. Lütfen tekrar giriş yapınız.",
                )

        response = await call_next(request)
        return response


def check_if_token_is_not_valid(request) -> bool:
    import fastapi_api.models
    token_is_not_valid = True

    token = request.headers.get("Authorization")
    if token:
        return token_is_not_valid

    return token_is_not_valid
