# Engine basics

PostgreSQL: databases, roles, grants, `pg_hba`, WAL. App user ≠ superuser. Migrations in Git (Flyway/Liquibase/Alembic).

Connection strings in Secrets Manager/Vault. SSL required.

Pooling: PgBouncer/RDS Proxy. Exhausted connections = app leak or missing pool.

Cache (Redis) is not the system of record.
