# absolute minimum time 10:00

### slide::
# !!{reset}  ▄█▀▀▀▄█   ▄▄█▀▀██   ▀██▀      !!{red}    █     ▀██          ▀██                                      !!{yellow} ██        ▄█▄
# !!{reset}  ██▄▄  ▀  ▄█▀    ██   ██       !!{red}   ███     ██    ▄▄▄▄   ██ ▄▄     ▄▄▄▄  ▄▄ ▄▄ ▄▄   ▄▄▄▄ ▄▄▄     !!{yellow}█  █      ██ ██
# !!{reset}   ▀▀███▄  ██      ██  ██       !!{red}  █  ██    ██  ▄█   ▀▀  ██▀ ██  ▄█▄▄▄██  ██ ██ ██   ▀█▄  █      !!{yellow}  ██      ██ ██
# !!{reset} ▄     ▀██ ▀█▄  ▀▄ ▀█  ██       !!{red} ▄▀▀▀▀█▄   ██  ██       ██  ██  ██       ██ ██ ██    ▀█▄█       !!{yellow} █        ██ ██
# !!{reset} █▀▄▄▄▄█▀    ▀█▄▄▄▀█▄ ▄██▄▄▄▄▄█ !!{red}▄█▄  ▄██▄ ▄██▄  ▀█▄▄▄▀ ▄██▄ ██▄  ▀█▄▄▄▀ ▄██ ██ ██▄    ▀█        !!{yellow}█▄▄▄  ██   ▀█▀
#                                                                                   !!{red} ▄▄ █
#                                                                                   !!{red}  ▀▀
#                               !!{letstalk}     █    █▀▀ ▀█▀ █ █▀▀   ▀▀█▀▀ █▀▀▄ █  █ ▄   █
#                               !!{letstalk}     █    █▀▀  █    ▀▀▄     █   █▄▄█ █  █▀▄   █
#                               !!{letstalk}     █▄▄█ ▀▀▀  ▀    ▀▀▀     █   █  █ ▀▀ ▀ ▀   ▄
#
#                           !!{letstalk} ░░░░░░▒▒▒▒▒▒██████ Presenter: Mike Bayer ██████▒▒▒▒▒▒░░░░░░
#                                 !!{letstalk} ░░░░░░▒▒▒▒▒▒██████ PWC  2023 ██████▒▒▒▒▒▒░░░░░░
# !!{reset}


### slide:: b
### title:: SQLAlchemy - What's in the Box
### * SQLAlchemy has always referred to itself as a "database toolkit"
### * The idea is, provide lots of tools.
### * One of these tools is an ORM
### * However there's also lots of other features that don't use the ORM

### slide:: b
### title:: SQLAlchemy - What's in the Box
### * Features like:
###     * A facade around the Python DBAPI that provides a much richer programming environment
###     * Database schema management functions
###     * a SQL query builder
###     * Schema inspection utilities
### * All of the above features that aren't "ORM" are called **SQLAlchemy Core**

### slide:: b
### title:: SQLAlchemy 2.0 - Brief History
### * When SQLAlchemy 1.3 was out for awhile, things needed to change.
### * First concepts for "something new" worked out in August-November 2018
### * The next few slides will talk about big changes from the 1.x to 2.0 SQLAlchemy series
### * novice users stand by....

### slide:: b
### title:: SQLAlchemy 2.0 - Brief History
### * Top level goals:
###      * Unify ``sqlalchemy.orm.Query`` with ``sqlalchemy.select()``
###      * Go all in on Python 3
###      * Get rid of "many ways to execute a SQL statement", troublesome "autocommit" feature
###      * All "top level" features / architectures would be in SQLAlchemy 1.4, except py3 only


### slide:: b
### title:: SQLAlchemy 2.0 - Brief History
### * Early Emergent goals:
###      * These goals became apparent as we began SQLAlchemy 1.4
###      * Integrate "baked" (SQL cached) queries within all statements across Core / ORM
###      * Implement pep-484 typing, first as stubs as well as a mypy plugin
###      * asyncio support using "stackless" (i.e. greenlet) technique
###      * 1.x -> 2.0 migration process using SQLALCHEMY_WARN_20=1 mode
###      * all "early" goals were released in SQLAlchemy 1.4
###      * 1.4.0b1 was November, 2020 (at 1.4.46 or so now)
###     * Got all the "risky" features out to the userbase, regressions were fixed, heavy lifting was done


### slide:: b
### title:: SQLAlchemy 2.0 - Brief History
### * Later Emergent goals:
###      * These goals became apparent as we started 2.0, after 1.4 was released
###      * Implement pep-484 typing inline
###      * New Declarative API to support pep-484 without Mypy plugins
###      * Embrace Python Dataclasses, taking advantage of pep-681 Dataclass Transforms
###      * SQL statements and result sets derive pep-484 typing from models
###      * High performance bulk INSERT feature for all backends
###      * Rearchitecture of Schema Reflection
###      * migrate C code to Cython
###      * SQLAlchemy 2.0b1 was released October, 2022


### slide:: b
### title:: The tutorial
### * The tutorial which follows is the latest version of the similar tutorial I and others have been doing since 2007
### * It maintains an emphasis on introduction of foundational concepts
### * For new users, the best prerequisite knowledge includes:
###      * general Python programming background
###      * Basic OOP terminology: classes, instances, methods, etc.
###      * Rudimentary SQL knowledge - run a SELECT statement, run an INSERT, run a CREATE TABLE
###      * Helpful: awareness of transactions and maybe the ACID model

### slide:: b
### title:: Onto the Tutorial!
### * any Q ?


### slide::
