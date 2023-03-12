# absolute minimum time 17:55


### slide:: b
### title:: Table Metadata
### * SQLAlchemy represents the structure of a relational schema using the concept of **table metadata**.
### * SQLAlchemy Core provides this, using a well known object called ``Table`` (along with lots of supporting objects)
### * The ``Table`` object can be constructed directly, and represents a table in a database.

### slide:: b
### title:: Table Metadata
### * As an example, it looks like this:

from sqlalchemy import Table, Column, MetaData
from sqlalchemy import DateTime, Integer, String

metadata = MetaData()

user_account_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("fullname", String),
    Column("created_at", DateTime),
)

### slide:: bi
### * Most official SQLAlchemy tutorials spend a lot of time on Table.
### * However, we're going to duck out the side entrance and go elsewhere...

### slide:: b
### title:: ORM Centric Table Metadata
### * In real world use, most applications are using the ORM to a greater or lesser degree
### * In most ORM applications, ``Table`` is constructed **indirectly** using a style known as **Declarative ORM**
### * Declarative ORM in SQLAlchemy 2.0 is super nice
### * ORM-Centric table metadata integrates with IDE typing tools, mypy, etc.
### * Creates typed SQL statements and result sets (!)
### * Integrates with Python dataclasses too
### * We can still do everything with Core as we did before

### slide:: b
### title:: ORM Centric Table Metadata - Declaration
### * The ORM mapping starts out with a base class called the **Declarative Base**

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass

### slide:: bi
### * When we make subclasses of Base, it generates an **ORM mapped class** that will refer to a database table
### * The ``MappedAsDataclass`` mixin is optional and indicates that the classes should also be Python dataclasses

### slide:: b
### title:: ORM Centric Table Metadata - Declaration

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)


### slide:: bi
### * Like dataclasses, typing information is derived at runtime from annotations
### * The ``Mapped[]`` type indicates to SQLAlchemy that an attribute is mapped to a database column
### * The ``mapped_column()`` construct is optional and allows additional details about the database column to be indicated
### * ``mapped_column()`` also receives the same arguments as ``dataclasses.field()``, like default, init, etc.

### slide:: b
### title:: ORM Centric Table Metadata - the Mapped Class
### * The User class is called a **Declarative Mapped Class**.
### * Since it's also a dataclass, it has methods like default ``__init__()`` and ``__repr__()`` based on the directives passed to ``mapped_column()``

User("spongebob", "Spongebob Squarepants")



### slide:: b
### title:: ORM Centric Table Metadata - the Table
### * The Declarative Mapped Class sets the ``Table`` for us, as the class is created
### * here it is

User.__table__


### slide:: bi
### * looks just like the ``Table`` we constructed directly

user_account_table


### slide:: bp
### title:: ORM Centric Table Metadata - Emitting DDL
### * Whether we made our ``Table`` directly or by using ORM Declarative, we can run a CREATE TABLE statement using a method ``.create_all()``

from sqlalchemy import create_engine

engine = create_engine("sqlite://")

with engine.begin() as conn:
    Base.metadata.create_all(conn)


### slide:: b
### title:: ORM Centric Table Metadata - Foreign Keys
### * We make a second ORM Declarative model (with its own ``Table``)
### * we will associate it to the User model using ``ForeignKey``


from sqlalchemy import ForeignKey


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))


### slide:: bp
### title:: ORM Centric Table Metadata - FOREIGN KEY
### * Emitting more DDL we see the FOREIGN KEY directive

with engine.begin() as conn:
    Base.metadata.create_all(conn)


### slide:: b
### title:: Core SQL (using ORM models)
### * The next two sections will illustrate the use of these ORM Models to create SQL statements
### * However, for SQLAlchemy veterans, note we are going to start with **Core only** use
### * We'll run INSERT, SELECT, and (in theory, if we had more slides) UPDATE and DELETE queries using ``Connection`` only, plain rows for results
### * Later, we will pull in the ORM ``Session``



### slide::
### title:: Questions?

### slide::
