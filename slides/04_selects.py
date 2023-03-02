### slide:: s

import termcolor
from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass
from sqlalchemy import create_engine, insert
from sqlalchemy import ForeignKey


_print = print


def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))



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

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))


engine = create_engine("sqlite://")
with engine.begin() as conn:
    Base.metadata.create_all(conn)
    uids = conn.scalars(
        insert(User).returning(User.id),
        [
            {"name": "spongebob", "fullname": "Spongebob Squarepants"},
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
            {"name": "squidward", "fullname": "Squidward Q Tentacles"},
            {"name": "pearl", "fullname": "Pearl Krabs"},
            {"name": "krabs", "fullname": "Mr. Krabs"},
        ],
    ).all()
    conn.execute(
        insert(Address),
        [
            {"user_id": uids[0], "email_address": "spongebob@sqlalchemy.org"},
            {"user_id": uids[1], "email_address": "sandy@sqlalchemy.org"},
            {"user_id": uids[1], "email_address": "pat999@aol.com"},
            {"user_id": uids[2], "email_address": "stentcl@sqlalchemy.org"},
        ]
    )


### slide:: b
### title:: SELECT statements
### * the basic unit to create a SELECT statement, if not using "text", is the ``sqlalchemy.select()`` function.
### * below we use it with another function ``literal()`` to create a SELECT for a single literal value

from sqlalchemy import select, literal
stmt = select(literal("some data"))

### slide:: bp
### title:: SELECT statements
### * Like we did with ``sqlalchemy.text()`` earlier, the ``select()`` construct can be executed using ``connection.execute()``

with engine.connect() as conn:
    print(conn.execute(stmt).scalars().one())


### slide:: b
### title:: SELECT statements
### * More interestingly, we can use our ORM models to create SELECTs against tables
### * The Class-bound attributes on ORM models represent SQL Columns, such as ``User.name`` below

stmt = select(User.name)

### slide:: bi
### * The above statement means, "select the 'name' column from the 'user_account' table"

print(stmt)

### slide:: bp
### title:: SELECT statements
### * We can get more columns...

stmt = select(User.id, User.name)
with engine.connect() as conn:
    print(conn.execute(stmt).all())

### slide:: bp
### title:: SELECT statements
### * ...whole tables...

stmt = select(User)
with engine.connect() as conn:
    print(conn.execute(stmt).all())


### slide:: bp
### title:: SELECT statements
### * multiple tables / columns with a JOIN (more on JOIN later)

stmt = select(User, Address.email_address).join_from(User, Address)
with engine.connect() as conn:
    print(conn.execute(stmt).all())


### slide:: b
### title:: WHERE criteria
### * class attributes like User.name are also the foundation of SQL expressions

print(User.name == 'spongebob')

### slide:: bi
### * above, the Python `__eq__()` operator was overridden to produce an expression object
User.name == 'spongebob'

### slide:: b
### title:: WHERE criteria
### * the generated expressions use **bound parameters** for all literal values.

print(User.name == 'spongebob')


### slide:: bi
### * the values for the parameters are embedded and come out during ``execute()``
### * for demonstration, they can be seen using a utility method called ``.compile()``

print(
    (User.name == 'spongebob')
    .compile(compile_kwargs={"literal_binds": True})
)


### slide:: b
### title:: more WHERE criteria
### * less than, greater than
print(User.name < 'spongebob')
print(User.name > 'spongebob')


### slide:: bi
### * IN expressions

print(
    User.name.in_(["spongebob", "sandy", "squidward"])

    # this is so we can see the full expression
    .compile(compile_kwargs={"literal_binds": True})
)

### slide:: bi
### * fancy string operators

print(User.name.icontains("spongebob"))


### slide:: b
### title:: WHERE criteria, ORDER BY, etc.
### * We can add these expressions as WHERE criteria using the ``.where()`` method

stmt = select(User.name).where(User.name.in_(["spongebob", "sandy", "squidward"]))

### slide:: bi
### * ``.where()`` (and most methods) can be called multiple times
stmt = stmt.where(User.id > 1)

### slide:: b
### title:: WHERE criteria, ORDER BY, etc.
### * expressions also go into other methods like ORDER BY via the ``.order_by()`` method

stmt = stmt.order_by(User.id)

### slide:: b
### title:: WHERE criteria, ORDER BY, etc.
### * expressions can also be selected; below we add a column expression

stmt = stmt.add_columns(literal("full name: ") + User.fullname)

### slide:: bip
### * Running the statement we see it all together

with engine.connect() as conn:
    for name, fullname in conn.execute(stmt):
        print(f"{name} {fullname}")


### slide:: b
### title:: FROM clauses, JOINs
### * The FROM clause of a SELECT derives from the columns / tables we select

print(select(User.name, Address.email_address))


### slide:: bp
### title:: FROM clauses, JOINs
### * FROM clause in less common cases can be set manually if needed using ``.select_from()``

stmt = select(func.count('*')).select_from(User)

with engine.connect() as conn:
    print(conn.scalar(stmt))


### slide:: bp
### title:: FROM clauses, JOINs
### * the ``.join_from()`` method produces a basic JOIN between two tables.
### * ON criteria for simple joins along foreign keys is usually automatic

stmt = select(User.name, Address.email_address).join_from(User, Address)

with engine.connect() as conn:
    for username, email in conn.execute(stmt):
        print(f"{username} {email}")

### slide:: bi
### * JOIN is more feature filled when working with ORM relationships, illustrated later

### slide:: b
### title:: UPDATE and DELETE, in brief
### * as a brief preview, UPDATE and DELETE statements have a target table like an INSERT...

from sqlalchemy import delete
from sqlalchemy import update

delete_stmt = delete(User)
update_stmt = update(User)

### slide:: bi
### * both have WHERE clauses like SELECT...

delete_stmt = delete_stmt.where(User.name == "krabs")
update_stmt = update_stmt.where(User.name == "patrick")


### slide:: bi
### * UPDATE additionally has "values" like INSERT, which is how we do the SET clause

update_stmt = update_stmt.values(fullname="Patrick Star")


### slide:: bp
### title:: UPDATE and DELETE, in brief
### * UPDATE and DELETE, like INSERT, need a ``.begin()`` block or ``.commit()`` to take effect

with engine.begin() as conn:
    conn.execute(delete_stmt)
    conn.execute(update_stmt)


### slide::
