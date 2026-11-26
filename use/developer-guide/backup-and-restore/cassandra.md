---
title: "Cassandra"
---

# Cassandra

SSTables live under the keyspace directory (default `/var/lib/cassandra/data/`), per the path in `cassandra.yaml`.

## Backup

::::: tabs
== Snapshot-based

Via `nodetool snapshot`, which flushes memtables and hard-links SSTables.

```bash
nodetool snapshot                                  # all keyspaces
nodetool snapshot -t 2023.06.27 organization       # one keyspace, named
nodetool snapshot --table employee organization    # one table
```

Transfer snapshots off-box (S3, GCS, Azure) afterward. `nodetool clearsnapshot` removes them locally.

::: warning
Snapshots don't back up the schema — do that separately.
:::

* *Advantages*: simple, easy to manage.
* *Disadvantages*: daily full-keyspace snapshots don't scale well for large datasets; transfer to cold storage can get expensive.

== Incremental

Set `incremental_backups: true` in `cassandra.yaml`. Cassandra then hard-links newly-flushed SSTables into a backup directory as they're written, on top of the last full snapshot.

* *Advantages*: lower disk usage, lower transfer cost.
* *Disadvantages*: Cassandra doesn't clean these up automatically (you need your own pruning script); produces many small files; can't selectively back up individual column families.
:::::

## Data Restore

:::: tabs
== nodetool refresh

Loads newly-placed SSTables without a restart.

1. Create the schema if missing
2. Truncate the table if needed
3. Copy the snapshot's SSTable directory into place
4. Run `nodetool refresh`

== sstableloader

Loads a set of SSTables into a running cluster — works for external data, existing SSTables, or snapshot restores:

```bash
sstableloader -d <ip> /home/data
```

Create the schema and truncate the table first if needed.
::::

