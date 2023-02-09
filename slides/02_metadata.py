### slide::
### title:: ORM Centric Schema and MetaData
# SQLAlchemy represents the structure of a relational schema
# using the concept of **table metadata**.   In most SQLAlchemy
# applications, table metadata is **declared** using ORM models,
# which are Python classes with attributes that represent columns

from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from datetime import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)


### slide::
# The User class is called a **Declarative Mapped Class**.   We've used
# MappedAsDataclass mixin, so this class is a standard Python dataclass,
# which we can construct using normal dataclass semantics:

User("spongebob", "Spongebob Squarepants")


### slide::
# The Declarative Mapped Class also sets up an internal structure called
# **table metadata**.  This consists of a type of object called
# Table, and we see it on our mapped class by looking
# at an attribute called __table__:


User.__table__


### slide::
# Table is part of SQLAlchemy's public API, and we can make Table objects
# directly.  However, using ORM Declarative models to declare
# Table definitions has the advantage of integration with pep-484 typing,
# both for declaration as well as providing type information for database
# results, and it will also set us up to be ready for the ORM sections
# later.


### slide::
# The Table knows all about what a real database table in the database
# looks like.  It has a collection of "columns":

list(User.__table__.c)

### slide:: i
# it also holds onto "constraints", the most basic of which is the primary
# key constraint:

User.__table__.primary_key



### slide:: p
# We can put together the Engine we did in the previous section with this
# new table-defining DeclarativeMappedClass to emit CREATE TABLE
# statements in a database:

from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)

with engine.begin() as conn:
    Base.metadata.create_all(conn)


### slide::
# If we want to have two tables related to each other, we use a
# construct called ForeignKey


from sqlalchemy import ForeignKey


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))


### slide:: p
# We can see the DDL here creates a table that includes a FOREIGN KEY
# constraint back to the other table

with engine.begin() as conn:
    Base.metadata.create_all(conn)




### slide::
### title:: Questions?

### slide::
