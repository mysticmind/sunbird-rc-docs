---
title: "PostgreSQL"
---

# PostgreSQL

Three backup methods, each with different tradeoffs.

| Method                      | Server downtime | Selective restore       | Portable across versions |
| --------------------------- | --------------- | ----------------------- | ------------------------ |
| SQL dump                    | No              | Yes (custom format)     | Yes                      |
| File-system-level           | Yes (full stop) | No — whole cluster only | No                       |
| Continuous archiving (PITR) | No              | Point-in-time           | No                       |

::::: tabs
== SQL Dump

```bash
pg_dump dbname > dumpfile      # backup
psql dbname < dumpfile         # restore
```

`pg_dump` produces an internally-consistent snapshot and is portable across PostgreSQL versions and architectures; it can run against a remote host with read access to the tables being backed up.

For restore, create the target database and ensure the relevant users exist first. `psql` continues past SQL errors by default — set `ON_ERROR_STOP` to change that:

```bash
psql --set ON_ERROR_STOP=on dbname < dumpfile
```

Pipe directly between servers:

```bash
pg_dump -h host1 dbname | psql -h host2 dbname
```

== File System Level

```bash
tar -cf backup.tar /usr/local/pgsql/data
```

::: warning
Limitations versus `pg_dump`: the server must be fully stopped for a usable backup (not just disallowing new connections), and you can't selectively restore individual tables — it's whole-cluster only, and the commit log files (`pg_xact/*`) must travel with the data files.
:::

An alternative is a filesystem-level consistent snapshot (if your filesystem supports it) — snapshot the volume, copy the data directory out, release the snapshot. This allows backing up while the server runs, but starting from that backup triggers WAL replay as if the server had crashed, so the WAL files must be included (and a `CHECKPOINT` beforehand shortens recovery). `rsync` is another option — sync while running, then a brief `rsync --checksum` during a short shutdown window minimizes downtime.

File-system backups tend to be larger than `pg_dump` output (which excludes index contents) but can be faster to take.

== Continuous Archiving (PITR)

Combining a file-system backup with archived WAL files (from `pg_wal/`) lets you recover to any point since the base backup: restore the file-system backup, then replay the archived WAL.

Benefits: the base backup doesn't need to be perfectly consistent (WAL replay fixes it), backups can be continuous rather than periodic full dumps, and a warm standby is achievable by continuously streaming WAL to another machine.

::: info
`pg_dump`/`pg_dumpall` can't participate in this scheme — they don't produce file-system-level backups with the metadata WAL replay needs.
:::
:::::

