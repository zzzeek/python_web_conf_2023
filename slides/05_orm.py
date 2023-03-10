### slide:: b
### title:: It's time for...
### * We now cross into a new dimension of everything thus far
### * Ready?

### slide:: i

# !!{letstalk}░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# !!{letstalk}░░░░░     ░░░░░░        ░░░░░   ░░░░░░░   ░░░░░░░           ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ░   ░
# !!{letstalk}▒▒▒   ▒▒▒▒   ▒▒▒   ▒▒▒▒   ▒▒▒  ▒   ▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒   ▒
# !!{letstalk}▒   ▒▒▒▒▒▒▒▒   ▒   ▒▒▒▒   ▒▒▒   ▒   ▒ ▒   ▒▒▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒▒    ▒   ▒   ▒▒▒▒▒   ▒▒▒▒▒   ▒   ▒
# !!{letstalk}▓   ▓▓▓▓▓▓▓▓   ▓  ▓   ▓▓▓▓▓▓▓   ▓▓   ▓▓   ▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓   ▓▓   ▓▓  ▓▓   ▓▓  ▓▓▓   ▓▓  ▓▓  ▓▓  ▓
# !!{letstalk}▓   ▓▓▓▓▓▓▓▓   ▓   ▓▓   ▓▓▓▓▓   ▓▓▓  ▓▓   ▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓   ▓▓   ▓▓  ▓▓   ▓         ▓▓  ▓▓  ▓▓  ▓
# !!{letstalk}▓▓▓   ▓▓▓▓▓   ▓▓   ▓▓▓▓   ▓▓▓   ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓   ▓▓   ▓▓  ▓▓   ▓  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# !!{letstalk}█████     ██████   ██████   █   ███████   ███████████   █████   █    ██  ██   ███     ████   █   █
# !!{letstalk}█████████████████████████████████████████████████████████████████████████████████████████████████████


### slide:: b
### title:: ORM Models, Again!


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

### slide:: p
### title:: create engine and generate the schema

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    Base.metadata.create_all(connection)

### slide:: b
### title:: Crossing from Core to ORM - Instances
### * We've already been working with ORM-Centric Metadata models
### * But we weren't really using "the ORM"
### * To use real ORM-centric patterns, we will add the use of **instances** of our ORM mapped classes
### * That is, while this is a class:

User

### slide:: bi
### * This, is an **instance** of a class:

spongebob = User("spongebob", "Spongebob Squarepants")
spongebob

### slide:: bi
### * Both are super important in the ORM - SQLAlchemy adds rich behaviors to both non-instantiated classes as well as instances of those classes


### slide:: b
### title:: Crossing from Core to ORM - the Session
### * For instances of User, we want to **persist** and **load** them to and from a database
### * To achieve this, we use a new kind of tool that can **mediate** between instances, SQL DML statements, and SQL result rows
### * all while maintaining these operations in an ongoing database transaction
### * This object is called **the Session**.
### * The ``Session`` is to the ORM what the ``Connection`` object is to Core - the "thing that interacts with the transaction"


### slide:: b
### title:: Crossing from Core to ORM - the Session
### * In a similar way as ``Connection`` objects come from a factory called ``Engine``; the ``Session`` comes from a factory called ``sessionmaker()``.
### * ``sessionmaker()`` is instantiated with an ``Engine``
### * This ``Engine`` is passed along to ``Session`` objects, which then use it to get database connections behind the scenes.

from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=engine)

### slide:: bi
### * The ``sessionmaker()`` creates a ``Session`` object when we just call it, like a callable:

session = session_factory()
session


### slide:: bp
### title:: sessionmaker, Session, and where's the database connection?
### * If ``sessionmaker()`` is a factory for ``Session`` like an ``Engine`` is a factory for ``Connection``, why isn't the method called ``session_factory.connect()``?
### * Because we didn't actually connect to anything yet.  The ``Session`` connects to database engines **on demand**, after it was instantiated.
### * as an example, we can make it connect right now by asking it for a database connection, using ``Session.connection()``
session.connection()


### slide:: bi
### * (The ``.connection()`` method is normally used in most real applications mmm ...hmmm... never.)

### slide:: bp
### title:: Session is connected, now what?
### * Once the ``Session`` has established a connection, it's considered to be **in a transaction**.
### * That same ``Connection`` object will continue to be used until the transaction ends
### * We can run any Core or ORM SQL statement using methods like ``Session.execute()`` (and friends ``Session.scalars()``, ``Session.scalar()``)

from sqlalchemy import text
result = session.execute(text("select 'hello world'"))

### slide:: bi
### * ``Session.execute()`` returns a ``Result`` object, just like ``Connection.execute()`` does as well.

print(result.first())

### slide:: bp
### title:: Session is connected, now what?
### * To end the transaction and **release** the ``Connection``, call:  ``Session.commit()``, ``Session.rollback()``, or ``Session.close()``

session.close()


### slide:: bp
### title:: Properly managing Session scope
### * Since ``Session`` has connect/close and begin/commit cycles, we normally want to use Python context manager patterns
### * ``sessionmaker()`` and ``Session`` integrate together to provide context manager support
### * Below, we open a ``Session``, run a statement in a block, then ``Session`` is closed

from sqlalchemy import select

with session_factory() as sess:
    print(sess.execute(select(User.id)).all())


### slide:: bp
### title:: Properly managing Session scope
### * ``sessionmaker()`` / ``Session`` support the same transaction patterns as ``Engine`` / ``Connection``
### * "commit-as-you-go", where we call ``Session.commit()`` any number of times

from sqlalchemy import insert

with session_factory() as sess:
    sess.execute(
        insert(User),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "gary", "fullname": "Gary the Snail"},
        ],
    )

    sess.commit()

### slide:: bp
### title:: Properly managing Session scope
### * and "begin once", where we call ``sessionmaker.begin()``, which establishes a new ``Session`` and provides a transaction-committing block

from sqlalchemy import delete

with session_factory.begin() as sess:
    sess.execute(delete(User))



### slide:: b
### title:: Unit of work patterns with the Session
### * Real world code should try to use context manager patterns to manage ``Session`` scope
### * However, for the **purposes of example**, we will make a single ``Session`` and leave it opened, so that interactions can be seen

session_that_we_will_keep_opened_only_for_the_purposes_of_example = session_factory()


### slide:: bi
### * Keep the above in mind as we continue!
session = session_that_we_will_keep_opened_only_for_the_purposes_of_example


### slide:: b
### title:: Unit of work patterns with the Session
### * Recall the User object we already made:

spongebob

### slide:: bi
### * We want to persist the data inside of "spongebob" into a new row in the "user_account" database table
### * We tell the ``Session`` this is what we want to do using ``Session.add()``

session.add(spongebob)

### slide:: b
### title:: Unit of work patterns with the Session
### * This did not yet modify the database, however the object is now referred towards as **pending**.
### * **pending** means, "this is a Python object that will be used to populate an INSERT statement"
### * We can see the "pending" objects by looking at the ``session.new`` attribute.

session.new


### slide:: b
### title:: Unit of work patterns with the Session
### * We have a "pending" object that will be used to populate an INSERT statement
### * The process by which the ``Session`` emits INSERT, UPDATE and DELETE statements for objects such as these is known as the **flush**
### * The flush process occurs when:
###     * We run any SQL statement with ``Session.execute()`` or similar, before that SQL statement is executed (known as **autoflush**)
###     * When any ORM instance runs a process known as "lazy loading" (also part of autoflush; more on that later)
###     * When we call an explicit method ``Session.flush()``
###     * When we commit the transaction with ``Session.commit()``, before the actual COMMIT occurs

### slide:: bp
### title:: Unit of work patterns with the Session
### * We will illustrate the flush occurring using "autoflush" behavior, by also loading an object **from** the database at the same time
### * This will persist the pending object we have and then load it right back in one step.
### * As seen previously, to SELECT rows from the database, we use ``select()``
### * The ``Session`` here has a new behavior we didn't see with ``Connection``; selecting a "User" will return **instances of User objects**, rather than individual columns

from sqlalchemy import select

select_statement = select(User).where(User.name == "spongebob")
result = session.execute(select_statement)

### slide:: b
### title:: Unit of work patterns with the Session
### * The ``Result`` that we get back from ``Session.execute()`` has a single row

row = result.first()

### slide:: bi
### * within this row, the ``User`` we selected is a single column value
also_spongebob = row[0]


### slide:: bi
### * On this ``User`` object, we see that server generated attributes ".id", ".created_at" are populated
also_spongebob

### slide:: b
### title:: Unit of work patterns with the Session
### * The User object we got back is also the **same Python object** as the original one we used with ``Session.add()``

spongebob
also_spongebob
spongebob is also_spongebob


### slide:: bi
### * The way that we got back the same object as the one we added is because the ``Session`` uses an ....?
### * <waits for class>
### * **Identity Map**


### slide:: b
### title:: The Identity Map
### * The **Identity Map** is a **weak mapping** of objects keyed to their class/primary key identity

dict(session.identity_map)


### slide:: bi
### * All objects that are persisted by the ``Session`` using "flush", as well as all objects that we load using ``Session.scalars()``, ``Session.execute()`` etc. are placed in the identity map
### * An object that is present in the identity map is said to be in the **persistent** state
### * **persistent** means, "there is a row in the current database transaction that matches this object's primary key identity"
### * It's an important integration point with all the ways that objects can be created and loaded


### slide:: b
### title:: Selecting objects with scalars
### * Recall how we had to extract our User object from a row

row[0]


### slide:: bip
### * We very frequently will want to load objects alone from our SELECT statements, not rows
### * So for everyday ORM "load objects" use, we will use ``Session.scalars()`` more often than ``Session.execute()``
### * We can run it here where we will still get the same "spongebob" object back

this_too_is_spongebob = session.scalars(select(User).where(User.name == "spongebob")).first()
print(this_too_is_spongebob)


### slide:: b
### title:: Unit of Work - Making Changes
### * ``Session.add_all()`` lets us add more objects into the **pending** state...

session.add_all(
    [
        User("patrick", "Patrick Star"),
        User("sandy", "Sandy Cheeks"),
    ]
)

### slide:: bi
### * as before, we can see these pending objects in ``Session.new``:

session.new

### slide:: b
### title:: Unit of Work - Making Changes
### * For objects that are already **persistent**, we can modify their attributes

spongebob.fullname = "Spongebob Jones"

### slide:: bi
### * Persistent objects that have Python-side changes on them are referred towards as **dirty**.
### * **dirty** objects can be seen in ``Session.dirty``

session.dirty

### slide:: bi
### * The **persistent, dirty** state for an object means "Python object with pending changes that will be used to populate an UPDATE statement"


### slide:: bp
### title:: Unit of Work - Committing changes
### * With objects in both the **pending** and **persistent** states, running any SQL operation, as well as any ``Session.flush()`` or ``Session.commit()`` call will "flush" all those changes before proceeding.

session.commit()

### slide:: bp
### title:: Unit of Work - Expire on commit, lazy loading, autobegin
### * The ``Session`` defaults to a behavior called **expire on commit**
### * It means that when the transaction is complete, all "data" is expired
### * When data is "expired", accessing object attributes again defaults to a behavior called **lazy loading**, i.e. refresh from the database
### * Refreshing from the database however needs a new transaction, so it calls upon a default behavior called **autobegin**
### * This means touching ``spongebob.fullname`` will start a new transaction and run a SELECT

spongebob.fullname

### slide:: b
### title:: Unit of Work - Controversy!
### * The expire-on-commit, lazy-loading, autobegin combination sums up most ORM controversy in a nutshell
### * The fundamental element is that these patterns allow for database IO without actually saying "run some IO"
### * Options exist to disable these features, e.g.:
###    * Turn off expire-on-commit: ``session_factory = sessionmaker(engine, expire_on_commit=False)``
###    * Turn off autobegin:  ``session_factory = sessionmaker(engine, autobegin=False)``
###    * Turn off lazy-loading: Turn off expiration + autobegin, use **eager loading** patterns as well as **raiseload** patterns



### slide::
### title:: Questions!


### slide::








