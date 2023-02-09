### slide::
### title:: Setup

# similar tables as before.  One change is how we are doing the
# default datetime for created_at, adding a SQL-time insert default.

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from datetime import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=datetime.utcnow,
        insert_default=datetime.utcnow
    )



class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))


### slide:: p
### title:: Create a database and tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)

with engine.begin() as conn:
    Base.metadata.create_all(conn)


### slide:: p
### title:: Inserting some Rows

from sqlalchemy import insert

insert_stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")

with engine.begin() as conn:
    conn.execute(insert_stmt)


### slide::
