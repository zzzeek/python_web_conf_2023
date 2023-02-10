### slide:: s

import termcolor
_print = print
def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))

### slide::
### title:: Setup

# similar tables as before.  One change is how we are doing the
# default datetime for created_at, adding a SQL-time insert default.

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=datetime.utcnow,
        server_default=func.now()
    )



### slide:: p
### title:: Create a database and tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://")

with engine.begin() as conn:
    Base.metadata.create_all(conn)


### slide::
### title:: Inserting some Rows
# The insert() construct can be used against a mapped entity or Core
# Table construct to produce an INSERT statement.

from sqlalchemy import insert

insert_stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")

print(insert_stmt)

### slide:: p
### title:: Inserting some Rows
# feed the INSERT statement to an execute() method to run it

insert_stmt = insert(User).values(name="spongebob", fullname="Spongebob Squarepants")

with engine.begin() as conn:
    conn.execute(insert_stmt)


### slide:: p
### title:: Inserting many rows at once
# The typical way we pass parameters to DML statements like INSERT
# is to send the "parameters" to the execute() method directly.  SQLAlchemy
# figures out what parameters to include in this mode, and knows a few ways to
# make this run more efficiently than just row-at-a-time

with engine.begin() as conn:
    conn.execute(
        insert(User),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "gary", "fullname": "Gary the Snail"},

        ],
    )


### slide:: p
### title:: Bonus Slide: SQLAlchemy 2.0 is very good at RETURNING
# in SQLAlchemy 2.0, most backends can deliver rows for us from an
# INSERT statement with the returned values.

with engine.begin() as conn:
    result = conn.execute(
        insert(User).returning(User),
        [
            {"name": "squidward", "fullname": "Squidward Q Tentacles"},
            {"name": "pearl", "fullname": "Pearl Krabs"},
            {"name": "krabs", "fullname": "Mr. Krabs"},
        ],
    )

    for row in result:
        print(f"New user added: {row.name}  Timestamp: {row.created_at}")


### slide::
