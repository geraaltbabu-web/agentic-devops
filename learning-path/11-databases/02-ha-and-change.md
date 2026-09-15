# HA and change

Multi-AZ: failover, not a backup. Snapshots + PITR. Test restore on a schedule.

Expand/contract: add column nullable → dual write → backfill → switch → drop old.

Blue/green app with incompatible schema = outage. Version the API.

Observability: slow queries, bloat, replication lag, failover events.
