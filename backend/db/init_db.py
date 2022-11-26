from sqlalchemy.orm import Session

from backend.db.base_class import Base
from backend.db import base
from backend.db.session import engine


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    print('Created db')
