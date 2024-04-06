from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

# from fastapi_api.validations import Login, Logout, ChangePassword, Remember, Forgot
# from fastapi_api.models import Users, UserToken, UserLoggedIn
#
# from fastapi_api.services import redis_cli, send_email
from sqlalchemy import or_


auth_route = APIRouter(prefix="/auth", tags=["Auth"])
auth_route.include_router(auth_route, include_in_schema=False)


