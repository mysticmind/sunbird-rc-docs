---
title: "Setup Backend"
---

# Setup Backend

<a href="https://github.com/Sunbird-RC" class="button primary" data-icon="github">Sunbird RC on GitHub</a> <a href="https://github.com/Sunbird-RC/devops/tree/main/deploy-as-code/helm" class="button secondary" data-icon="github">Deployment files</a>

| What                        | Where                                                                                                                                                                                              |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend repos               | [github.com/Sunbird-RC](https://github.com/Sunbird-RC)                                                                                                                                             |
| Kubernetes deployment files | [`Sunbird-RC/devops`](https://github.com/Sunbird-RC/devops/tree/main/deploy-as-code/helm), with the [README here](https://github.com/Sunbird-RC/devops/blob/main/deploy-as-code/helm/v1/README.md) |
| Schemas                     | [`sunbird-rc-core/java/registry/src/main/resources/public/_schemas`](https://github.com/Sunbird-RC/sunbird-rc-core/tree/main/java/registry/src/main/resources/public/_schemas)                     |

::: info
The `_schemas` directory doesn't show up in a GitHub file browse — git doesn't track empty directories — but it's the live default `SCHEMA_DIR` mount point in `docker-compose.yml`. You're expected to populate it yourself.
:::

