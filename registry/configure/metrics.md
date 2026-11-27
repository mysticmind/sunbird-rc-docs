---
title: "Metrics"
---

# Metrics

Sunbird RC can emit `ADD`/`UPDATE`/`DELETE`/`READ` events from the registry, in the Sunbird telemetry event format. Enable with `event_enabled=true`, set `event_topic`, and set `event_providerName` to one of the providers below.

Sample event:

```json
{
  "eid": "ADD", "ets": 1678958110872, "ver": "3.1", "mid": "abc-123",
  "actor": { "id": "123", "type": "User" },
  "context": { "channel": "sunbird-rc-core", "env": "dev" },
  "object": { "id": "xyz-123", "type": "Student" },
  "edata": { "...": "entity fields, masked per the schema's privateFields/internalFields config" }
}
```

:::: tabs
== Kafka-based

`event_providerName=dev.sunbirdrc.registry.service.impl.KafkaEventService`

The registry publishes to the configured topic (default `events`); a consumer stores it in Clickhouse. Entity data is masked per the schema's `privateFields`/`internalFields` config.

== File-based

`event_providerName=dev.sunbirdrc.registry.service.impl.FileEventService.java`

Events are appended to `metrics_log/metrics.log`, with a 30 MB rolling policy.
::::

## Metrics Service

The Kafka consumer, using Clickhouse by default:

```sql
create table <table_name> (
  operationType String,
  createdAt Date,
  entityId String,
  entity JSON
)
```

One table per distinct schema type. Exposes two APIs: an event-count API (across all tables) and an aggregates API — a cron job computes aggregates and caches them in Redis, served from there. Configure the cron with `CRON_ENABLE`, `SCHEDULE_INTERVAL` (days), `SCHEDULE_TIME` (GMT).

::: info
See the [full discussion](https://github.com/orgs/Sunbird-RC/discussions/) for the end-to-end interaction diagram.
:::

