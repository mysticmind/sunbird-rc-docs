---
title: "Custom Keycloak Build"
---

# Custom Keycloak Build

SunbirdRC uses a custom Keycloak image that makes NONCE validation toggleable — a change not available in stock Keycloak, added specifically to support Digilocker Meripehchaan SSO ([tracking issue](https://github.com/Sunbird-RC/community/issues/593)).

<a href="https://github.com/Sunbird-RC/keycloak/tree/configurable-nonce-validation" class="button primary" data-icon="github">Sunbird RC/keycloak</a> <a href="https://github.com/Sunbird-RC/keycloak/blob/configurable-nonce-validation/docs/building.md" class="button secondary">Build docs</a>

::: info
NONCE validation is on by default; set `VALIDATE_NONCE=false` to disable it.
:::

**Prerequisites**: JAVA 11 (tested with 11.0.8), Maven.

:::: steps
::: step
### Build the distribution jar

```bash
git clone https://github.com/Sunbird-RC/keycloak/tree/configurable-nonce-validation
mvn clean install -Pdistribution
```

Output lands in `distribution/server-dist/target`.
:::

::: step
### Build the Docker image

```bash
git clone https://github.com/keycloak/keycloak-containers/tree/main/
git checkout 14.0.0
cd server
python -m http.server 8001
docker build -t sunbirdrc/keycloak --build-arg KEYCLOAK_DIST=http://<YOUR_IP_ADDRESS>:8001/keycloak-14.0.0.tar.gz .
```
:::

::: step
### Push it

Tag and push to your Docker registry.
:::
::::

