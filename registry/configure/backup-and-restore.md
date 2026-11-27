---
title: "Backup and Restore"
---

# Backup and Restore

Sunbird RC can connect to a range of data sources, as covered in [the High-Level Architecture page](/registry/architecture/high-level-architecture).

::: warning
Beyond the primary database, also plan backups for Kafka, ElasticSearch, and Filestore if you use them.
:::

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>PostgreSQL</strong></td><td>SQL dump, file-system-level backup, and continuous archiving with PITR.</td><td><a href="broken://pages/pNVtxcZ6eK1ynS7NtCxl">Broken link</a></td></tr><tr><td><strong>Cassandra</strong></td><td>Snapshot and incremental backups, plus the two restore methods.</td><td><a href="broken://pages/oYUi2uPVJrcBn6onLvOd">Broken link</a></td></tr></tbody></table>
