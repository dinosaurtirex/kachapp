# Create DB

```
CREATE USER cache_holder WITH PASSWORD 'abobus';
CREATE DATABASE cacha_db;

ALTER ROLE cache_holder SET client_encoding TO 'utf8';
ALTER ROLE cache_holder SET default_transaction_isolation TO 'read committed';
ALTER ROLE cache_holder SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE cacha_db TO cache_holder;
GRANT ALL ON DATABASE cacha_db TO cache_holder;
ALTER DATABASE cacha_db OWNER TO cache_holder;
```

```
aerich init -t settings.TORTOISE_ORM
aerich init-db
aerich migrate --name init
aerich upgrade
```