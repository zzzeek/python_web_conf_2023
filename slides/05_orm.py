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
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass
from sqlalchemy import ForeignKey

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)

### slide::
### title:: create engine and metadata

### slide::
### title:: set up Session

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


### slide::
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

















