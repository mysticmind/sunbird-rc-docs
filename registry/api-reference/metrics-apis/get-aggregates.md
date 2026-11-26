---
title: "Get Aggregates"
---

# Get Aggregates

## This API will emit the aggregates of events that occurred in the specified time period. Time period can be configured in the metrics service using configurations

<mark style="color:var(--vp-c-indigo-1);">`GET`</mark> `http://localhost:8070/v1/aggregates`&#x20;

:::: tabs
== 200: OK Object with aggregates over the period of configured time. Eg {schema: {add: 3, delete: 1}}}
::::

