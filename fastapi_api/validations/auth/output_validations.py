from pydantic import BaseModel, EmailStr


class UserLoginResponse(BaseModel):
    access_token: str
    refresher_token: str
