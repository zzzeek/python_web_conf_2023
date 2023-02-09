### slide:: s
import os
from sqlalchemy import create_engine
from sqlalchemy import text


### slide::
### title:: Engine Basics
# create_engine() builds a *factory* for database connections.
# Below we create an engine that will connect to a SQLite database.

from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)


### slide::
# The Engine doesn't actually connect until we tell it to for the first
# time.  When using it directly, we get a connection using the .connect()
# method.

connection = engine.connect()
connection

### slide::
# The Connection is a so-called **proxy** for a DBAPI connection.  We can
# see it by peeking at the .connection.driver_connection attribute

connection.connection.driver_connection

### slide:: p

# The Connection then features an .execute() method that will run queries.
# To invoke a textual query we use the text() construct

from sqlalchemy import text

stmt = text("select 'hello world' as greeting")
result = connection.execute(stmt)

### slide::
# the result object we get back is similar to a cursor, with more methods,
# such as first() which will return the first row and close the result set
row = result.first()

### slide:: i
# the row looks and acts mostly like a named tuple
row
row[0]
row.greeting

### slide::
# it also has a dictionary interface, which is available via an accessor
# called ._mapping
row._mapping["greeting"]


### slide:: p
# common idiomatic Python patterns including iteration and tuple
# assignment are available (and likely the most common usage)
result = connection.execute(
    text("select * from (values (1, 'hello'), (2, 'hola'), (3, 'bonjour'))")
)
for id_, greeting in result:
    print(f"id: {id_}   greeting: {greeting}")

### slide:: p
# there's also other methods like all().   More methods will be discussed
# later.
result = connection.execute(
    text("select * from (values (1, 'hello'), (2, 'hola'), (3, 'bonjour'))")
)
result.all()

### slide::
# Connection has a .close() method.  This **releases** the
# DBAPI connection back to the connection pool.  This typically
# does not actually close the DBAPI connection unless the pool is
# in overflow mode.
connection.close()

### slide:: p
# Usually, modern Python code should manage the connect/release process
# using context managers.

with engine.connect() as connection:
    print(connection.execute(text("select 'hello' as greeting")).all())

### slide:: p
### title:: transactions, committing

# Unlike previous SQLAlchemy versions, SQLAlchemy 2.0 has no concept
# of "library level" autocommit; which means, if the DBAPI driver is in
# a transaction, SQLAlchemy will never commit it automatically.   The usual
# way to commit is called "commit as you go"

with engine.connect() as connection:
    connection.execute(
        text("create table employee (emp_id integer primary key, emp_name varchar, fullname varchar)")
    )

    insert_stmt = text("insert into employee(emp_name, fullname) values (:name, :fullname)")

    connection.execute(
        insert_stmt,
        {"name": "spongebob", "fullname": "Spongebob Squarepants"}
    )
    connection.commit()


### slide:: p
# the other way is called "begin once", when you just have a single transaction
# to commit

with engine.begin() as connection:
    connection.execute(
        insert_stmt,
        {"name": "patrick", "fullname": "Patrick Star"}
    )

 # end of block: commits transaction, releases connection back to the
 # connection pool. rolls back if there is an exception before re-throwing


### slide:: p
# You can also use begin() blocks local to the connection
#
with engine.connect() as connection:
    with connection.begin():
        connection.execute(
            insert_stmt,
            {"name": "krabs", "fullname": "Mr. Krabs"}
        )
    # end of inner block: commits transaction, or rollback if exception
 # end of outer block: releases connection to the connection pool


### slide:: p
# autocommit can be achieved using the AUTOCOMMIT isolation level:

with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
    connection.execute(
        insert_stmt,
        {"name": "squidward", "fullname": "Squidward Q. Tentacles"}
    )


### slide::
### title:: Questions?

### slide::
