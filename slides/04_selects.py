# absolute minimum time 23:04

### slide:: s

from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass
from sqlalchemy import create_engine, insert, func
from sqlalchemy import ForeignKey


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
### * In the section on executing statements with an ``Engine``, we ran a ``text()`` construct that looked like this:

from sqlalchemy import text
stmt = text("select 'hello world' as greeting")

### slide:: bi
### * let's write that instead using SQLAlchemy's Core expression language, using a construct called ``select()``.
### * In order to select a literal value like "hello world" we will also use a construct called ``literal()``.

from sqlalchemy import select, literal

stmt = select(
    literal("hello world").label("greeting")
)

### slide:: bp
### title:: SELECT statements
### * As we did previously with ``text()``, we can run this statement using ``Connection.execute()``

with engine.connect() as connection:
    result = connection.execute(stmt)
    print(result.first())

### slide:: bi
### * note that ``literal()`` automatically made the use of a bound parameter for the string "hello world".  Most SQLAlchemy SQL constructs will automatically use bound values as much as possible.

### slide:: b
### title:: SELECT statements
### * While selecting a plain string seemed a bit cumbersome, usually we are using ``select()`` to SELECT from tables and columns
### * As we are using ORM-Centric table metadata, the class-bound attributes on ORM models represent SQL Columns, such as ``User.name`` below, which we can SELECT from.

stmt = select(User.name)

### slide:: bi
### * The above statement means, "select the 'name' column from the 'user_account' table"

print(stmt)

### slide:: b
### title:: SELECT statements - what are we SELECTing?
### * The arguments we send to ``select()`` are a series of columns, tables (or a corresponding ORM mapped class), other so-called "selectables" like aliases or subqueries, and SQL expressions
### * Examples of ``select()`` include:
### * SELECT from a whole table
print(select(User))

### slide:: bi
### * SELECT from a series of columns
print(select(User.id, User.name, User.created_at))

### slide:: b
### title:: SELECT statements - what are we SELECTing?
### * SELECT from a series of tables/columns from more than one table
print(select(User.name, User.fullname, Address.email_address))

### slide:: bi
### * as we see in that last statement, the FROM clause expands to include all tables we are SELECTing from

### slide:: b
### title:: SELECT statements - what are we SELECTing...FROM?
### * When selecting from multiple tables we normally want to JOIN them together.  A straightforward way to do this is to use the ``select().join_from()`` method

stmt = select(User.name, User.fullname, Address.email_address).join_from(User, Address)
print(stmt)

### slide:: bx
### title:: SELECT statements - what are we SELECTing...FROM?
### * ``join_from()`` will normally generate the ON criteria based on the presence of the ``ForeignKey`` construct in table metadata
### * Recall from the "metadata" chapter that we defined User / Address roughly like this:

"""
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    # ...

class Address(Base):
    __tablename__ = "address"
    # ...
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
"""

### slide:: bi
### * the ``Address.user_id`` which links to ``ForeignKey("user_account.id")`` gives ``join_from()`` what it needs to know

### slide:: bp
### title:: SELECT statements - what are we SELECTing...FROM?
### * Putting it together we can get a structured display of both tables at once
stmt = select(User.name, User.fullname, Address.email_address).join_from(User, Address)

with engine.connect() as connection:
    result = connection.execute(stmt)
    for row in result:
        print(f"{row.name:15} {row.fullname:25}  {row.email_address}")

### slide:: bp
### title:: SELECT statements - we are...SELECTing!
### * Finally, there's a whole world of more complex SELECT statements using aliases, subqueries, etc.
### * Such as, "SELECT user names that have more than one email address"

email_address_count = (
    select(Address.user_id, func.count(Address.email_address).label('email_count')).group_by(Address.user_id).
    having(func.count(Address.email_address) > 1).subquery()
)
stmt = select(User.name, email_address_count.c.email_count).join_from(User, email_address_count)

with engine.connect() as connection:
    for row in connection.execute(stmt):
        print(f"username: {row.name} | number of email addresses: {row.email_count}")


### slide:: b
### title:: SELECT statements - limiting rows with WHERE criteria
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
### * the values for the parameters are embedded and come out during ``Connection.execute()``
### * for demonstration, they can be seen using a utility method called ``.compile()``

print(
    (User.name == 'spongebob')
    .compile(compile_kwargs={"literal_binds": True})
)


### slide:: b
### title:: SELECT statements - limiting rows with WHERE criteria
### * less than, greater than
print(User.name < 'spongebob')
print(User.name > 'spongebob')

### slide:: bi
### * fancy string operators

print(User.name.icontains("spongebob"))


### slide:: b
### title:: SELECT statements - limiting rows with WHERE criteria
### * IN expressions

print(
    User.name.in_(["spongebob", "sandy", "squidward"])

    # this is so we can see the full expression
    .compile(compile_kwargs={"literal_binds": True})
)



### slide:: b
### title:: SELECT statements - limiting rows with WHERE criteria, ordering with ORDER BY
### * We can add these expressions as WHERE criteria using the ``.where()`` method

stmt = select(User.name).where(User.name.in_(["spongebob", "sandy", "squidward"]))
print(stmt)

### slide:: bi
### * ``.where()`` can be called multiple times; criteria is joined by AND
stmt = stmt.where(User.id > 1)
print(stmt)

### slide:: b
### title:: WHERE criteria, ORDER BY, etc.
### * expressions also go into other methods like ORDER BY via the ``.order_by()`` method

stmt = stmt.order_by(User.id)

### slide:: b
### title:: SELECT statements - limiting rows with WHERE criteria, ordering with ORDER BY
### * expressions can also be selected; below we add a column expression

stmt = stmt.add_columns(literal("full name: ") + User.fullname)

### slide:: bip
### * Running the statement we see it all together

with engine.connect() as conn:
    for name, fullname in conn.execute(stmt):
        print(f"name: {name:15} {fullname}")


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


### slide:: b
### title:: SQL expression language - sum up
### * The SQL expression language intends to allow **any SQL structure** to be modeled as a Python expression
### * SQLAlchemy goes very far with this concept; topics not covered here include UNIONs, CTEs, window functions, set-returning functions, OLAP operators
### * When writing SQLAlchemy SQL expressions, the hope is that one can be thinking in terms of SQL statements, not "translation"
### * Using Python objects for SQL expressions allows fluid composability, database agnosticism to a greater or lesser degree

### slide::
### * Questions?