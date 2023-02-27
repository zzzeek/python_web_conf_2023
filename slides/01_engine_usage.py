### slide:: s
import os
from sqlalchemy import create_engine
from sqlalchemy import text
import sys

import termcolor
_print = print
def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))


### slide:: b
### title:: Engine Basics - An Engine is a Factory
### * create_engine() builds a *factory* for database connections.
### * In the following example, we create an engine that will connect to a SQLite database.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")


### slide:: b
### title:: Engine Basics - Our First Connection
### * The Engine doesn't actually connect until we tell it to for the first time.
### * When using Engine directly, we get a connection using the .connect() method.

connection = engine.connect()
connection

### slide:: b
### title:: Engine Basics - Our First Connection
### * The Connection is a so-called **proxy** for a DBAPI connection.
### * In this case, the DBAPI is Python's sqlite3 module
### * We can see it by peeking at the .connection.driver_connection attribute:

connection.connection.driver_connection

### slide:: bp
### title:: Engine Basics - Execute a SQL String
### * The SQLAlchemy Connection then features an .execute() method that will run queries, using the underlying DBAPI connection and cursor behind the scenes.
### * To invoke a textual query, use the text() construct, passed to .execute():

from sqlalchemy import text

stmt = text("select 'hello world' as greeting")
result = connection.execute(stmt)

### slide:: b
### title:: Engine Basics - Getting Results
### * The Connection.execute() method **always** returns a Result object.
### * In this specific case it's called CursorResult, which means it's a direct proxy for a DBAPI cursor

result

### slide:: b
### title:: Engine Basics - Getting Results
### * The Result is similar to a DBAPI cursor, but has more methods, transformations, and automation.
### * One method is first(), which will return the first row and close the result set:
row = result.first()
row

### slide:: b
### title:: Engine Basics - Getting Results
### * the row looks and acts mostly like a named tuple:
row
row[0]
row.greeting

### slide:: bi
### * it also has a dictionary interface, which is available via an accessor called ._mapping
row._mapping["greeting"]


### slide:: pb
### title:: Engine Basics - Getting Results
### * common idiomatic Python patterns including iteration and tuple assignment are common
result = connection.execute(
    text("select * from (values (1, 'hello'), (2, 'hola'), (3, 'bonjour'))")
)
for id_, greeting in result:
    print(f"id: {id_}   greeting: {greeting}")

### slide:: pb
### title:: Engine Basics - Getting Results
### * for the very common case of getting an iterator of single values, the Connection.scalars() or Result.scalars() methods are recommended
for greeting in connection.scalars(
    text("select * from (values ('hello'), ('hola'), ('bonjour'))")
):
    print(f"greeting: {greeting}")

### slide:: pb
### title:: Engine Basics - Getting Results
### * there's also other methods like all().
result = connection.execute(
    text("select * from (values (1, 'hello'), (2, 'hola'), (3, 'bonjour'))")
)
result.all()

### slide:: pb
### title:: Engine Basics - Getting Results
### * all() and other result methods work with scalars() too
scalar_result = connection.scalars(
    text("select * from (values ('hello'), ('hola'), ('bonjour'))")
)
scalar_result.all()

### slide:: b
### title:: Engine Basics - Closing Connections
### * Connection has a .close() method.
### * .close() **releases** the DBAPI connection back to the connection pool.
### *  "releases" means the pool may hold onto the connection, or close it if it's part of overflow
connection.close()

### slide:: bp
### title:: Engine Basics - Closing Connections
### * Modern use should favor context managers to manage the connect/release process

with engine.connect() as connection:
    print(connection.execute(text("select 'hello' as greeting")).all())

### slide:: b
### title:: Engine Basics - Transactions, Committing
### * SQLAlchemy 2.0 always assumes an explicit or implicit "begin" of a "transaction", at the start of some SQL operations
### * and it then expects an explicit "commit" or "rollback" at the end of those operations
### * There's no "library level" "autocommit"; SQLAlchemy 2.0 **never** emits COMMIT implicitly
### * however, true "autocommit" at the driver level is supported, where no explicit COMMIT is needed

### slide:: bp
### title:: Engine Basics - Transactions, Committing
### * The Connection has two variations in how this "transaction" starts.
### * One is called "commit as you go" - as SQL is run, a transaction starts, which can be committed using Connection.commit()

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


### slide:: bp
### title:: Engine Basics - Transactions, Committing
### * The other variation is called "begin once" - the transaction starts as an explicit block that commits when complete

with engine.begin() as connection:
    connection.execute(
        insert_stmt,
        {"name": "patrick", "fullname": "Patrick Star"}
    )

 # end of block: commits transaction, releases connection back to the
 # connection pool. rolls back if there is an exception before re-throwing


### slide:: bp
### title:: Engine Basics - Transactions, Committing
### * engine.connect() can also be used with connection.begin()
with engine.connect() as connection:
    with connection.begin():
        connection.execute(
            insert_stmt,
            {"name": "krabs", "fullname": "Mr. Krabs"}
        )
    # end of inner block: commits transaction, or rollback if exception
 # end of outer block: releases connection to the connection pool


### slide:: bp
### title:: Engine Basics - Transactions, Committing
### * To use autocommit, this is enabled as an **execution option** on the Connection or Engine
### * The programming patterns and code structure **do not change** at all
### * There is still a client-side notion of a "transaction".
### * The DBAPI driver COMMITs all statements implicitly

with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
    connection.execute(
        insert_stmt,
        {"name": "squidward", "fullname": "Squidward Q. Tentacles"}
    )


### slide::
### title:: Questions?

### slide::
