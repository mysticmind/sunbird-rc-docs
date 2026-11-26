---
title: "Digilocker Meripehchaan SSO"
---

# Digilocker Meripehchaan SSO

To surface the Digilocker Meripehchaan SSO login button, use Keycloak's own login theme instead of the default custom theme.

::: info
**Prerequisites**

* Keycloak
* A [DigiLocker partner account](https://www.digilocker.gov.in/web/partners/)
* Client secrets generated via [APISetu's DigiLocker resource center](https://apisetu.gov.in/digilocker)
* Redirect URL set to `<domain>/auth/realms/master/broker/oidc/endpoint`
:::

:::: steps
::: step
### Add the identity provider in Keycloak

Keycloak admin page (`<domain>/auth/`) → Identity Providers → Add provider → **OpenID Connect v1.0**.
:::

::: step
### Set the endpoints

| Setting               | Value                                                              |
| --------------------- | ------------------------------------------------------------------ |
| Authorization URL     | `https://digilocker.meripehchaan.gov.in/public/oauth2/1/authorize` |
| Token URL             | `https://digilocker.meripehchaan.gov.in/public/oauth2/2/token`     |
| Disable User Info     | On                                                                 |
| Client Authentication | Client secret sent as post                                         |
| Prompt                | consent                                                            |
| Use PKCE              | Enabled, method `S256`                                             |

Set the Client Id / Client Secret generated in the DigiLocker partner portal.
:::

::: step
### Enable the default Keycloak theme

Clients → `registry-frontend` → Login Theme → `keycloak` → Save.
:::
::::

