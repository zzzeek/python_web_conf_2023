# absolute minimum time 11:53

### slide:: s

import termcolor
_print = print
def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))


### slide:: b
### title:: Inserts
### * In this section, we'll illustrate the ``insert()`` construct, which directly corresponds to a SQL INSERT statement
### * We will start with an ORM-Centric Metadata model that is mostly the same as that of the previous section.

### slide:: b
### title:: Inserts - ORM-Centric Model

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
        init=False, server_default=func.now()
    )

### slide:: bi
### * The above model features one change, which is a **server default** set up on the created_at column

### slide:: bp
### title:: Inserts - Get an Engine and create tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://")

with engine.begin() as conn:
    Base.metadata.create_all(conn)

### slide:: bi
### * Above, we can see the server default of "CURRENT_TIMESTAMP" generated for the created_at column
### * This will allow new date values to be generated for any INSERT statement encountered by the server which doesn't already include this column


### slide:: b
### title:: The insert() construct
### * The ``insert()`` function starts with a single argument; the table, or table-representing ORM entity, that is the target of the INSERT.
### * In this case it's the User class
### * The ``Table`` object that is part of the User class will be used behind the scenes to build a SQL INSERT statement

from sqlalchemy import insert

insert_stmt = insert(User)

### slide:: bi
### * Next, we further indicate a VALUES clause to be included in the INSERT statement, using the ``insert.values()`` method
### * ``insert.values()`` in this form accepts keys that match database column names

insert_stmt = insert_stmt.values(name="spongebob", fullname="Spongebob Squarepants")

### slide:: b
### title:: The insert() construct
### * With that, we can stringify this object to illustrate the general SQL structure we'll be sending to the database.

print(insert_stmt)

### slide:: bi
### * The actual data is inside the ``insert()`` object, and will be passed to the database as parameters
### * We can see the data in this case using a utility method called ``.compile()``

print(insert_stmt.compile(compile_kwargs={"literal_binds": True}))


### slide:: bp
### title:: Executing the insert statement
### * We use ``engine.begin()`` to create a transaction block that will commit at the end
### * Then in the block, ``.execute()`` the statement


with engine.begin() as conn:
    conn.execute(insert_stmt)


### slide:: b
### title:: INSERT using "executemany"
### * The previous example used ``.values()`` which produces a specific VALUES clause.
### * For simple cases, we usually rely upon SQLAlchemy itself to generate this for us
### * SQLAlchemy generates the VALUES clause, if not otherwise given, based on a collection of parameters passed to the ``.execute()`` method separately
### * Then, we can pass a **dictionary** or **list of dictionaries** to the ``.execute()`` method to accompany the statement
### * SQLAlchemy will then INSERT lists of dictionaries in bulk

### slide:: bp
### title:: INSERT using "executemany"
### * The automatic generation of VALUES works by inspecting the keys within the first dictionary given
### * The convention of "keys match column names" is the same as that of the ``insert.values()`` method.

with engine.begin() as conn:
    conn.execute(
        insert(User),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "gary", "fullname": "Gary the Snail"},
        ],
    )


### slide:: bp
### title:: Bonus Slide: SQLAlchemy 2.0 is very good at RETURNING
### * There's more INSERT can do
### * But here we will just illustrate a fairly exciting new feature in SQLAlchemy 2.0
### * Insert lots of rows with RETURNING at the same time (on almost every backend)

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
