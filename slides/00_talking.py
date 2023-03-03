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
###     * sleepless devs (yes there are more of me now) answering questions 24/7
### * All of the above features that aren't "ORM" are called **SQLAlchemy Core**
### * The most curmudgeonly DBA should have no problem with all the things that are in Core
### * but alas, they are curmudgeonly....

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
###      * Implement pep-484 typing, first as stubs
###      * asyncio support using "stackless" technique
###      * all "early" goals were released in SQLAlchemy 1.4
###      * 1.4.0 was November, 2020 (at 1.4.46 or so now)


### slide:: b
### title:: SQLAlchemy 2.0 - Brief History
### * Later Emergent goals:
###      * These goals became apparent as we started 2.0, after 1.4 was released
###      * Implement pep-484 typing inline
###      * New Declarative API to support pep-484 without Mypy plugins
###      * Embrace Python Dataclasses, taking advantage of pep-681 Dataclass Transforms
###      * SQL statements and result sets derive typing from models
###      * High performance INSERT..VALUES..RETURNING for all backends
###      * Rearchitecture of Schema Reflection
###      * migrate C code to Cython


### slide:: b
### title:: SQLAlchemy 2.0 - The Migration
### * SQLAlchemy 1.4
###     * Implemented all the "top level" and "early emergent" goals
###     * Core / ORM execution model *completely* rewritten for ``select()`` unification, caching
###     * No seriously, this was incredibly difficult.  months and months of staring into the void...
###     * New 2.0 APIs presented in a fully "opt-in" way
###     * SQLALCHEMY_WARN_20=1 mode, inspired by 2to3
###     * Had all the "risky" features, very long regression period as we fixed statement caching / ORM Query regressions

### slide:: b
### title:: SQLAlchemy 2.0 - The Migration
### * SQLAlchemy 2.0
###     * With all the heavy lifting done in 1.4 and released for ongoing battle testing, we could then work on "lighter" things
###     * Remove all Python 2 code (hooray!)
###     * totally new pep-484 inline typing
###     * new ORM Declarative that works with pep-484
###     * Dataclasses ORM integration
###     * new bulk INSERT features
###     * Other things: schema reflection architecture, Cython


### slide:: b
### title:: Onto the Tutorial!
### * any Q ?


### slide::
