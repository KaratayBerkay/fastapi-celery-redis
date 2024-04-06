from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, TIMESTAMP
from .database import session, Base
from sqlalchemy_mixins.session import SessionMixin
from sqlalchemy_mixins.inspection import InspectionMixin


class BaseMixin(Base, SessionMixin, InspectionMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[str] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"[{self.__class__.__name__}] {self.id}"

    @classmethod
    def filter(cls, *arg):
        return cls.query.filter(*arg).populate_existing()

    def delete(self):
        self.session.delete(self)
        self.session.commit()
        self.session.flush()

    def save(self):
        try:
            self.session.add(self)
            self.session.commit()
            self.session.flush()
            return self
        except Exception as e:
            print(f"Session veriyi kaydetmedi {e}")
            self.session.rollback()


BaseMixin.set_session(session)
