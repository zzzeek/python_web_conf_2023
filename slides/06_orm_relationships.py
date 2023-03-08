### slide:: b
### title:: relationships
### * In this mapping we add a second class and declare a **relationship** between the two classes
### * ORM relationships are defined using an ORM function called ``relationship()``, and allow ORM mapped classes to refer to each other
### * The ``relationship()`` defines an abstraction on top of database foreign keys, which indicate how table rows can refer to each other
### * Setup will take a few slides so first the imports + declarative base

from datetime import datetime
from typing import Optional
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass



### slide:: b
### title:: relationships - the User class (the "one" side)
### * Next, we make the User class as in other sections.  The last line has something new, a **relationship** called "addresses"
### * This is configured using the ``relationship()`` function, along with an annotation that names the target class and collection type
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", default_factory=list
    )

### slide:: bi
### * The User.addresses ``relationship()`` indicates a reference to a list of Address objects.

### slide:: b
### title:: relationships - the Address class (the "many" side)

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email_address: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), init=False)
    user: Mapped["User"] = relationship(back_populates="addresses", default=None)


### slide:: bi
### * We can see that just like User refers to Address, Address also refers to User, however it refers to User in two different ways
###     * it has a ``ForeignKey()`` on the "user_id" column, that refers to the User.id column.  This is the **schema level** declaration of the relationship
###     * It has a ``relationship()`` on the "user" attribute, that refers to the User class.  This is the **orm level** declaration of the relationship
### * We also see that this ``relationship()`` as well as the other one names a parameter ``back_populates``.  More on this in a moment

### slide:: bp
### title:: relationships
### * Before we proceed, setup an Engine, CREATE TABLE, and a Session

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    Base.metadata.create_all(connection)

from sqlalchemy.orm import sessionmaker
session_factory = sessionmaker(engine)

### slide:: bx
### title:: relationships
### * Our User / Address example features two separate ``relationship()`` constructs in a **bi-directional** configuration
### * User.addresses, which refers to a list of Address objects...

"""
class User(Base):

    # ... non-running-example...

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", default_factory=list
    )
"""

### slide:: bix
### * and Address.user, which is a reference to a User object.

"""
class Address(Base):

    # ... non-running-example...

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), init=False)
    user: Mapped["User"] = relationship(back_populates="addresses", default=None)
"""

### slide:: b
### title:: relationships - one-to-many, many-to-one
### * The Address.user_id column is a **foreign key** to User.id
### * This means there can be **many** Address objects that refer to **one** user
### * So we say that Address.user is a **many to one** relationship
### * Flipping it over, **one** user can have **many** Address objects
### * So we also say that User.address is a **one to many** relationship
### * When dealing with one-to-many or many-to-one, the table with the **foreign key CONSTRAINT is on the "many" side**
### * The table that has the **primary key column(s) that the foreign key points to is on the "one" side**

### slide:: b
### title:: Using relationship at the class level in queries
### * Recall how we used ``join_from()`` to join between User and Address:
from sqlalchemy import select
print(select(User.name, Address.email_address).join_from(User, Address))

### slide:: bi
### * The above JOIN uses the ``ForeignKey()`` on ``Address``
### * With ``relationship()``, we can join more succinctly and specifically using ``select().join()`` with the class-bound attribute
print(select(User.name, Address.email_address).join(User.addresses))


### slide:: bi
### * ``relationship()`` does a lot more than that for queries, however ``.join()`` is the most common usage


### slide:: bx
### title:: relationships - back_populates
### * Each ``relationship()`` has an attribute name, and a ``back_populates`` naming the other direction

"""
class User(Base):

    # ... non-running-example...

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", default_factory=list
    )

class Address(Base):

    # ... non-running-example...

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), init=False)
    user: Mapped["User"] = relationship(back_populates="addresses", default=None)
"""

### slide:: bi
### * ``back_populates`` indicates that these two relationships will be kept in sync with each other
### * ``back_populates`` is optional, but if two relationships are mirrors of one another, it should be included


### slide:: b
### title:: Creating instances with relationships
### * First create a User object as we always have

mr_krabs = User("krabs", "Mr. Krabs")

### slide:: bi
### * The User object has a default list that we've given it, which is empty

mr_krabs.addresses


### slide:: bi
### * Let's then make three Address objects

a1, a2, a3 = (
    Address(email_address="krabs@gmail.com"),
    Address(email_address="k25@yahoo.com"),
    Address(email_address="krabs@hotmail.com")
)

### slide:: bi
### We can add these to the mr_krabs.addresses list (or replace the list)
mr_krabs.addresses.extend([a1, a2, a3])

### slide::
# "back populates" sets up Address.user for each User.address.

a1.user
a2.user

### slide::
# adding User->squidward will *cascade* each Address into the Session as well.

session = session_factory()

session.add(mr_krabs)
session.new

### slide:: p
# commit.
session.commit()


### slide:: bp
### title:: Relationships load themselves on instances
### * When we access an unloaded relationship, the default behavior it uses is **lazy load**

mr_krabs.addresses

### slide:: bi
### * The lazy load is both useful and problematic, depending on context
### * The ORM query guide has a comprehensive section on **eager loading** and other relationship loading techniques, at https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html



### slide::
