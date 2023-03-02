### slide:: s

import termcolor
_print = print
def print(text):
    _print(termcolor.colored(text, attrs=["bold"]))

### slide:: b
### title:: ORM Centric Table Metadata
### * SQLAlchemy represents the structure of a relational schema using the concept of **table metadata**.
### * Commonly, table metadata is **declared** using ORM-enabled Python classes
### * SQLAlchemy 2.0's **Declarative** style has much resemblance to Python dataclass syntax
### * SQLAlchemy classes also integrate with dataclasses, which is optional (but so far seems very popular)

### slide:: b
### title:: ORM Centric Table Metadata - Declaration
### * The ORM mapping starts out with a base class called the **Declarative Base**

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass

### slide:: bi
### * When we make subclasses of Base, it generates an ORM mapped class that will refer to a database table
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
### * Since it's also a dataclass, it has methods like default constructor and repr based on the field directives

User("spongebob", "Spongebob Squarepants")



### slide:: b
### title:: ORM Centric Table Metadata - the Table
### * The Declarative Mapped Class also sets up an internal structure called ``sqlalchemy.Table``
### * This is an example of **table metadata** and represents the structure of a database table:

User.__table__


### slide:: b
### title:: ORM Centric Table Metadata - the Table
### * ``Table`` is part of SQLAlchemy's public API
### * Traditional Core-only SQLAlchemy use involves ``Table`` objects directly, without using ORM classes at all
### * However, Core-only programs can use ORM Declarative models for table metadata now.
### * This offers some advantages, even when not using the ORM:
###      * integration with pep-484 typing, IDEs
###      * type information for database result sets
###      * statements are cross-compatible with Core / ORM

### slide:: bp
### title:: ORM Centric Table Metadata - Emitting DDL
### * Putting together the ``Table`` with an `Engine``, we can automate the production of CREATE TABLE statements

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
### * We'll run INSERT, SELECT, UPDATE, DELETE queries using ``Connection`` only, plain rows for results
### * Later, we will pull in the ORM ``Session``



### slide::
### title:: Questions?

### slide::
