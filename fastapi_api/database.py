from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


engine_config = {
    "url": WagDatabase.DATABASE_URL,
    "pool_size": 10,
    "max_overflow": 0,
    "echo": False,
}

engine = create_engine(**engine_config)
session_config = {"autoflush": True, "bind": engine, "echo": True}
SessionLocal = sessionmaker(**session_config)
session = scoped_session(sessionmaker(bind=engine))
session.expunge_all()

Base = declarative_base()
