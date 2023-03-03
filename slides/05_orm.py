### slide:: s

import termcolor


_print = print


def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))



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
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)

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
### * Both are super important in the ORM - SQLAlchemy adds rich behaviors to both non-instantiated classes as well as instances


### slide:: b
### title:: Crossing from Core to ORM - the Session
### * For instances of User, we want to **persist** and **load** them to and from a database
### * To achieve this, we use a new kind of tool that can **mediate** between instances, SQL DML statements, and SQL result rows
### * all while maintaining these operations in an ongoing database transaction
### * This object is called **the Session**, or ``Session``.
### * It's analogous to the ORM as the ``Connection`` object is analogous to Core.


### slide:: b
### title:: Crossing from Core to ORM - the Session
### * In a similar way that ``Connection`` comes from a factory for connections known as ``Engine``, the ``Session`` comes from a factory called ``sessionmaker()``.
### * ``sessionmaker()`` is given our ``Engine``, which it will use when it needs to get database connections

from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=engine)

### slide:: bi
### * The ``sessionmaker()`` creates a ``Session`` object when we just call it, like a callable:

session = session_factory()
session


### slide:: bp
### title:: sessionmaker, Session, and where's the database connection?
### * Why isn't it ``Session.connect()``?
### * Because we didn't actually connect to anything yet.  The ``Session`` connects to database engines **on demand**.
### * as an example, we can make it connect right now by asking it for a database connection, using ``.connection()``
session.connection()


### slide:: bip
### * (The ``.connection()`` method is normally used in most real applications mmm ...hmmm... never.)

### slide:: bp
### title:: Session is connected, now what?
### * Once the ``Session`` has established a connection, it's considered to be **in a transaction**.
### * This transaction stays until we call:  ``.commit()``, ``.rollback()``, or ``.close()``

session.close()


### slide:: b
### title:: Properly managing Session scope
### * Since ``Session`` has a connect/close cycle, we normally want to use Python context manager patterns
### * ``sessionmaker()`` and ``Session`` integrate together to provide context manager support
### * Below we open a ``Session``, run a statement in a block, then ``Session`` is closed

from sqlalchemy import select

with session_factory() as sess:
    print(sess.execute(select(User.id)).all())


### slide:: bp
### title:: Properly managing Session scope
### * ``sessionmaker()`` supports the same transaction modes as the engine
### * "commit-as-you-go", where we call ``.commit()`` any number of times

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

### slide:: bip
### * and "begin once", where we call ``.begin()`` that runs a transaction block

from sqlalchemy import delete

with session_factory.begin() as sess:
    sess.execute(delete(User))



### slide:: b
### title:: Unit of work patterns with the Session
### * For most of these examples, we will make a single ``Session`` and leave it opened, so that interactions can be seen
### * Real world code should try to use context manager patterns to manage ``Session`` scope

session_that_we_will_keep_opened_only_for_the_purposes_of_example = session_factory()


### slide:: bi
### * Keep the above in mind as we continue!
session = session_that_we_will_keep_opened_only_for_the_purposes_of_example


### slide:: b
### title:: Unit of work patterns with the Session
### title:: Make pending objects


### slide::
### title:: inspection

### slide::
### title:: add objects


### slide::
### title:: inspection again


### slide::
### title:: query for pending object, flush

### slide::
### title:: identity map

### slide::
### title:: modify object


### slide::
### title:: commit

### slide::
### title:: invalidate

### slide::
### title:: bad changes


### slide::
### title:: rollback
















