---
title: "Tech Stack and Requirements"
description: "Software versions and infrastructure needed to run the Sunbird RC registry."
---

# Tech Stack and Requirements

Software versions and infrastructure needed to run the Sunbird RC registry.

## Architecture diagram

```mermaid
block-beta
    columns 5
    Mobile["Mobile app"]
    block:Web:4
        columns 4
        WebTitle["Web portal"]:4
        CoreUI["Sunbird RC Core UI"] Overrides["UI overrides"] Keycloak["Keycloak theme"] CustomUI["Custom UI"]
    end
    API["REST APIs"]:5
    RC["Sunbird RC"]:5
    classDef title fill:none,stroke:none,font-weight:bold
    classDef box fill:#dbe8f6,stroke:#4a7bab,color:#1d1d1f
    classDef api fill:#fcd9d9,stroke:#c0504d,color:#1d1d1f,font-weight:bold
    classDef rc fill:#d9f2d9,stroke:#3f8f3f,color:#1d1d1f,font-weight:bold
    class WebTitle title
    class Mobile,CoreUI,Overrides,Keycloak,CustomUI box
    class API api
    class RC rc
```

## Tech stack

<table><thead><tr><th width="284">Software / language</th><th>Recommended</th><th>Minimum version</th></tr></thead><tbody><tr><td>Java</td><td>11</td><td>11</td></tr><tr><td>Go</td><td>1.25.0</td><td>1.25.0</td></tr><tr><td>Linux </td><td>24.04 LTS</td><td>22.04 LTS</td></tr><tr><td>Docker</td><td>29.8.1</td><td>25.0.0</td></tr><tr><td>PostgreSQL</td><td>18.6</td><td>14</td></tr><tr><td>Redis</td><td>8.8.3</td><td>7.4.9</td></tr><tr><td>Elasticsearch</td><td>6.8.23</td><td>6.8.23</td></tr><tr><td>Keycloak</td><td>14.0.0</td><td>14.0.0</td></tr><tr><td>MinIO</td><td>RELEASE.2025-10-15T17-29-55Z</td><td>RELEASE.2025-10-15T17-29-55Z</td></tr><tr><td>Kafka (Zookeeper)</td><td>7.9.6</td><td>7.9.6</td></tr><tr><td>nginx</td><td>1.30.4</td><td>1.30.0</td></tr><tr><td>Angular</td><td>10</td><td>10</td></tr><tr><td>Kubernetes</td><td>1.37.0</td><td>1.35.0</td></tr><tr><td>Helm</td><td>4.2.4</td><td>4.0.0</td></tr><tr><td>Docker Compose</td><td>5.5.1</td><td>2.0.0</td></tr></tbody></table>

## Stock frontend interface

Angular 10

## Deployment

* **Local machine:** Docker is recommended.
* **Development:** A single VM with Docker will work. See [Getting started](broken://pages/ZnkzbsrphUupNhUbjFau) for setup steps.
* **Production:** Kubernetes is recommended. See the typical requirements below.

## Typical production requirements

<table><thead><tr><th width="220">Component</th><th width="100">Nodes</th><th>Specification</th></tr></thead><tbody><tr><td>UI (backed by CDN)</td><td>1 (small)</td><td>2 core, 4 GB RAM minimum</td></tr><tr><td>Kubernetes cluster</td><td>3</td><td>4 core, 8 GB RAM, 200 GB storage</td></tr><tr><td>PostgreSQL</td><td>2</td><td>4 core, 8 GB RAM, 500 GB storage</td></tr><tr><td>Elasticsearch (if needed)</td><td>1</td><td>4 core, 8 GB RAM, 200 GB storage</td></tr><tr><td>Load balancer</td><td>—</td><td>Based on cloud provider</td></tr></tbody></table>
