from models.database import Base


class BaseMixin(Base):
    __abstract__ = True


