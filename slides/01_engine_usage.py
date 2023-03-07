# absolute minimum time 20:00

### slide:: s
from sqlalchemy import create_engine
from sqlalchemy import text


### slide:: b
### title:: Engine Basics - An Engine is a Factory
### * Before we build lots of things, let's just connect to a database.
### * The innermost "connect to the database" structure is called the ``Engine``.
### * This is the most foundational construct in SQLAlchemy Core.
### * To get an ``Engine``, we use the ``sqlalchemy.create_engine()`` function:

from sqlalchemy import create_engine

engine = create_engine("sqlite://")

### slide:: bi
### * In the above example, we made an ``Engine`` that will connect to a SQLite memory database.
### * We didn't actually connect yet; the ``Engine`` is instead a **factory** that makes new connections when used
### * The ``Engine`` also stores a **connection pool**, where connections we use will be reused for subsequent operations

### slide:: b
### title:: Engine Basics - Our First Connection
### * The ``Engine`` doesn't actually connect until we tell it to for the first time.
### * When using ``Engine`` directly, we get a connection using the ``.connect()`` method.

connection = engine.connect()

### slide:: bi
### * The returned object is an instance of ``sqlalchemy.engine.Connection``:
connection

### slide:: b
### title:: Engine Basics - Our First Connection
### * The ``sqlalchemy.engine.Connection`` is a so-called **proxy** for a DBAPI connection.
### * In this case, the DBAPI is Python's sqlite3 module
### * We can see it by peeking at the ``.connection.driver_connection`` attribute:

connection.connection.driver_connection

### slide:: bp
### title:: Engine Basics - Execute a SQL String
### * The SQLAlchemy ``Connection`` then features an ``.execute()`` method that will run queries, using the underlying DBAPI connection and cursor behind the scenes.
### * To invoke a textual query, use the ``sqlalchemy.text()`` construct, passed to ``.execute()``:

from sqlalchemy import text

stmt = text("select 'hello world' as greeting")
result = connection.execute(stmt)

### slide:: b
### title:: Engine Basics - Getting Results
### * The ``Connection.execute()`` method **always** returns a ``sqlalchemy.engine.Result`` object.
### * In this specific case it's called ``CursorResult``, which means it's a direct proxy for a DBAPI cursor

result

### slide:: b
### title:: Engine Basics - Getting Results
### * The ``Result`` is similar to a DBAPI cursor, but has more methods, transformations, and automation.
### * One method is ``.first()``, which will return the first row (or None if no row) and close the result set:
row = result.first()

### slide:: b
### title:: Engine Basics - Getting Results
### * The row is a ``sqlalchemy.engine.Row`` object
type(row)

### slide:: bi
### * the ``Row`` object looks and acts mostly like a named tuple:
row
row[0]
row.greeting

### slide:: bi
### * it also has a dictionary interface, which is available via an accessor called ``._mapping``
row._mapping["greeting"]


### slide:: bx
### title:: Engine Basics - Getting Results QUICKSLIDE
### * To get lots of rows back, patterns include iteration
for row in result:
    print(row)

### slide:: bix
### * Tuple assignment with iteration
for id_, greeting in result:
    print(f"id: {id_}   greeting: {greeting}")

### slide:: bix
### * Iterate through first column of each row
for greeting in result.scalars():
    print(f"greeting: {greeting}")

### slide:: bix
### * get all rows in a list
list_of_rows = result.all()

### slide:: bix
### * get all first columns in a list
list_of_scalars = result.scalars().all()


### slide:: b
### title:: Engine Basics - Closing Connections
### * ``Connection`` has a ``.close()`` method.
### * ``.close()`` **releases** the DBAPI connection back to the connection pool.
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
### * One is called "commit as you go" - as SQL is run, a transaction starts, which can be committed using ``Connection.commit()``

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
### * ``engine.connect()`` can also be used with ``connection.begin()``
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
### * To use autocommit, this is enabled as an **execution option** on the ``Connection`` or ``Engine``
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
