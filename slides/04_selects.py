### slide:: s

import termcolor

_print = print


def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))

### slide::
### title:: SELECT statements
# same User ORM mapped class as the previous section.

from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=datetime.utcnow, server_default=func.now()
    )


### slide:: p
### title:: Create some data that we can SELECT from

from sqlalchemy import create_engine, insert

engine = create_engine("sqlite://")
with engine.begin() as conn:
    Base.metadata.create_all(conn)
    conn.execute(
        insert(User),
        [
            {"name": "spongebob", "fullname": "Spongebob Squarepants"},
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "gary", "fullname": "Gary the Snail"},
            {"name": "squidward", "fullname": "Squidward Q Tentacles"},
            {"name": "pearl", "fullname": "Pearl Krabs"},
            {"name": "krabs", "fullname": "Mr. Krabs"},
        ],
    )




### slide::
### title:: SELECT statements
# Using Declarative ORM models to represent table metadata, the
# class-bound attributes on the class have special behavior where they
# represent a SQL column

User.name

### slide::
### title:: SELECT statements
# representing a SQL column means we can for example create a SELECT
# statement from one or more, using the SQLAlchemy select() function

from sqlalchemy import select
stmt = select(User.name)


### slide:: i
# this object means to select the "name" column from the "user_account"
# table.

print(stmt)

### slide:: p
### title:: SELECT statements
# what we normally do with these objects is execute them.   Using
# Core, we can use connection.execute()

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)


### slide::
### title:: WHERE criteria
# the next special thing about class bound attributes like User.name is that
# we can make SQL expressions out of them, using standard Python operators
# like ==

print(User.name == 'spongebob')

### slide:: i
# we can see that the Python `__eq__()` operator was overridden to produce
# a SQLAlchemy-specific expression object
User.name == 'spongebob'

### slide::
# the generated expressions use **bound parameters** for all literal values.

print(User.name == 'spongebob')


### slide:: i
# the name is in there however, which we can see if we stringify the
# statement using a utility method called .compile()

print(
    (User.name == 'spongebob')
    .compile(compile_kwargs={"literal_binds": True})
)


### slide::
### title:: WHERE criteria
# more operators

# less than, greater than

print(User.name < 'spongebob')
print(User.name > 'spongebob')


### slide:: i
# IN expressions

print(
    User.name.in_(["spongebob", "sandy", "squidward"])

    # this is so we can see the full expression
    .compile(compile_kwargs={"literal_binds": True})
)

### slide:: i
# fancy string operators

print(User.name.icontains("spongebob"))


### slide:: p
### title:: WHERE criteria
# we put together the select() + criteria using the where() method

stmt = select(User.name).where(User.name.in_(["spongebob", "sandy", "squidward"]))

with engine.connect() as conn:
    print(conn.scalars(stmt).all())



### slide::
