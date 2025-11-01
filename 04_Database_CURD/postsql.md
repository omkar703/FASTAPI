# postsql

- postsql is an open-source relational database management system (RDBMS) that emphasizes extensibility and SQL compliance.

- It is designed to handle a wide range of workloads, from small single-machine applications to large internet-facing applications with many concurrent users.

## Features

- **Extensibility**: Users can define their own data types, operators, and index types.
- **ACID Compliance**: Ensures reliable transactions with Atomicity, Consistency, Isolation
  , and Durability.

- **ORM**: object relational mapper translates between a programming language python and database

- **SQLAlchemy** : is the most popular ORM for python mapping objects to database tables and providing a high-level SQL language
  - SQLModel it can integrate with SQLAlchemy and the pydantic
  - SQLModel design for the FastAPI

# create a session

if we want a session then we need to create a session class
SQLalchemy for AsyncSession ->session class -> session obj

# for secured file transfer between user and the database we create a migration this called version file where the changes are reflected

here use alembic for that
alembic init -t async migrations

for run -> alembic revision --autogenerate -m "init"
