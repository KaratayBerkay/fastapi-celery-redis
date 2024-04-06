import uvicorn
import routers

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException

from configs import Config
from middlewares.token_middleware import AuthHeaderMiddleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_app = FastAPI(title=str(Config.TITLE), default_response_class=JSONResponse)


@api_app.get("/", include_in_schema=False, summary=str(Config.DESCRIPTION))
async def home():
    return RedirectResponse(url="/docs")


for router in routers.__all__:
    if getattr(routers, router):
        api_app.include_router(getattr(routers, router))

openapi_schema = get_openapi(
        title=Config.TITLE,
        description=Config.DESCRIPTION,
        version="0.0.1",
        routes=api_app.routes,
    )

if "components" in openapi_schema:
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "evyos-session-key",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
        }
    }

for route in api_app.routes:
    path = str(getattr(route, "path"))
    if route.include_in_schema:
        methods = [method.lower() for method in getattr(route, "methods")]
        for method in methods:
            if path not in Config.INSECURE_PATHS:
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]
                openapi_schema["paths"][path][method]["responses"]["403"] = {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/HTTPValidationError"
                            }
                        }
                    },
                    "description": "Returned if user is unauthorized.",
                }

api_app.openapi_schema = openapi_schema


def exception_handler(exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.__str__()}
    )


api_app.add_middleware(
    CORSMiddleware,
    **{
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
)
api_app.add_middleware(AuthHeaderMiddleware)
api_app.add_exception_handler(Exception, exception_handler)


if __name__ == "__main__":
    uvicorn_config = {
        "app": "app:api_app",
        "host": "0.0.0.0",
        "port": 40111,
        "log_level": "info",
        "reload": True,
    }
    uvicorn.Server(uvicorn.Config(**uvicorn_config)).run()
