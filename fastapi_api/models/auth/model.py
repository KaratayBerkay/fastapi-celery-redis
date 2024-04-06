import jwt
import bcrypt
from ..mixin import BaseMixin
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from configs import Config


class Users(BaseMixin):

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False, comment="Name")
    surname: Mapped[str] = mapped_column(String, nullable=False, comment="Surname")
    email: Mapped[str] = mapped_column(String, nullable=False, comment="Email")
    hashed_password: Mapped[str] = mapped_column(String, nullable=False, comment="Hashed Password")

    def save_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.save()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    def save_token(self):
        access_token = jwt.encode({"user": self.id}, Config.SECRET_KEY, algorithm="HS256")
        refresher_token = jwt.encode({"user": self.id, "http_info": {}}, "secret", algorithm="HS256")
        return {
            "access_token": access_token,
            "refresher_token": refresher_token,
        }


