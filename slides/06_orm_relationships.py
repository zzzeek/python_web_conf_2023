### slide:: b
### title:: relationships


from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass, relationship
from sqlalchemy import ForeignKey

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    addresses: Mapped["Address"] = relationship(back_populates="user", default=None)

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

### slide::
### title:: create engine and metadata

### slide::
### title:: sessionmaker

### slide::
### title:: make object with relationship

### slide::
### title:: backref



### slide::
### title:: add / cascade


### slide::
### title:: query

### slide::
### title:: query w selectinload

### slide::
### title:: joins



### slide::


