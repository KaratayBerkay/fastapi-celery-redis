from fastapi import status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi_api.validations import UserLoginRequest, UserLoginResponse

from sqlalchemy import or_
from models import Users, Tokens

auth_route = APIRouter(prefix="/auth", tags=["Auth"])
auth_route.include_router(auth_route, include_in_schema=False)


@auth_route.post("/login", response_model=UserLoginResponse, description="Kullanıcı girişi")
def auth_login(login: UserLoginRequest):
    found_user: Users = Users.filter(Users.email == login.email).first()

    if not found_user:
        raise Exception("Kullanıcı bulunamadı.")

    if not found_user.check_password(login.password):
        raise Exception("Şifre hatalı.")

    tokens = found_user.save_token()
    if not tokens:
        raise Exception("Token oluşturulamadı.")

    return UserLoginResponse(
        access_token=tokens.get("access_token"),
        refresher_token=tokens.get("refresher_token")
    )
