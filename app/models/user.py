from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import (INTEGER, TEXT, TIMESTAMP)


from app.models import BasePostgres


class DBSchema:
    __table_args__ = {'schema': 'db'}


class User(BasePostgres, DBSchema):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    fname = Column(TEXT)
    lname = Column(TEXT)
    created = Column(TIMESTAMP, default=datetime.now())
