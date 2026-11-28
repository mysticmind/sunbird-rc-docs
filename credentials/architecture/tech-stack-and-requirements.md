---
title: "Tech Stack and Requirements"
description: "Software versions needed to run Sunbird RC credentialling services."
---

# Tech Stack and Requirements

Software versions needed to run Sunbird RC credentialling services.

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

<table><thead><tr><th width="284">Software / language</th><th>Recommended</th><th>Minimum version</th></tr></thead><tbody><tr><td>Node.js</td><td>20.20.2</td><td>20.11.0</td></tr><tr><td>Linux</td><td>24.04 LTS</td><td>22.04 LTS</td></tr><tr><td>Docker</td><td>29.8.1</td><td>25.0.0</td></tr><tr><td>PostgreSQL</td><td>18.6</td><td>14</td></tr><tr><td>nginx</td><td>1.30.4</td><td>1.30.0</td></tr><tr><td>Kubernetes</td><td>1.36.4</td><td>1.35.0</td></tr><tr><td>Helm</td><td>4.2.3</td><td>4.0.0</td></tr><tr><td>Docker Compose</td><td>5.5.1</td><td>2.0.0</td></tr></tbody></table>
