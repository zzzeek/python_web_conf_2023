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
#                     !!{letstalk} ░░░░░░▒▒▒▒▒▒██████       Presenter: Mike Bayer       ██████▒▒▒▒▒▒░░░░░░
#                           !!{letstalk} ░░░░░░▒▒▒▒▒▒██████ @zzzeek@fosstodon.org ██████▒▒▒▒▒▒░░░░░░
#                                 !!{letstalk} ░░░░░░▒▒▒▒▒▒██████ PWC  2023 ██████▒▒▒▒▒▒░░░░░░
#
#                                   Download this entire interactive tutorial at:
#
#                                   !!{bold}https://github.com/zzzeek/python_web_conf_2023
#
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
### title:: The tutorial
### * The tutorial which follows is the latest version of the similar tutorial I and others have been doing since 2007
### * It maintains an emphasis on introduction of foundational concepts, here given in 2.0 terms
### * For new users, the best prerequisite knowledge includes:
###      * general Python programming background
###      * Basic OOP terminology: classes, instances, methods, etc.
###      * Rudimentary SQL knowledge - run a SELECT statement, run an INSERT, run a CREATE TABLE
###      * Helpful: awareness of transactions and maybe the ACID model

### slide:: b
### title:: Ridiculously important links
### * We are trying **very hard** to make the most important documentation findable
### * #1 issue, user "could not find" documentation
### * Here are the most important links (download this talk from github to copy)
###     * **Documentation index:** https://docs.sqlalchemy.org/
###     * **Quickstart:** https://docs.sqlalchemy.org/en/latest/orm/quickstart.html
###     * **Unified Tutorial:** https://docs.sqlalchemy.org/en/latest/tutorial/index.html
###     * **ORM Querying Guide:** https://docs.sqlalchemy.org/en/latest/orm/queryguide/index.html

### slide:: b
### title:: Onto the Tutorial!


### slide::
