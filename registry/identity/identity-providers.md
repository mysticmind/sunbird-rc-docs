---
title: "Generic IAM"
---

# Generic IAM

SunbirdRC was originally tightly coupled to Keycloak. It now supports any OAuth2-compliant identity layer for both purposes an IAM platform serves here: authN/authZ between user and entity, and managing the user accounts created for entities.

## Configure the registry core

```bash
oauth2_resource_uri=https://domain/auth/
oauth2_resource_email_path=email
oauth2_resource_consent_path=consent
oauth2_resource_roles_path=realm_access.roles
oauth2_resource_entity_path=entity
```

| Platform   | `oauth2_resource_uri`                            |
| ---------- | ------------------------------------------------ |
| Keycloak   | `https://keycloak-domain/auth/realms/sunbird-rc` |
| Auth0      | `https://xxxx.us.auth0.com/` (API domain)        |
| FusionAuth | The tenant's configured issuer URL               |

## Enabling user-account creation on a new IAM platform

SunbirdRC ships **three** submodules under [`java/middleware/registry-middleware`](https://github.com/Sunbird-RC/sunbird-rc-core/tree/main/java/middleware/registry-middleware):

| Submodule      | Keycloak                                           | auth0                                       | generic-iam                                       |
| -------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------------- |
| Path           | `java/middleware/registry-middleware/keycloak`     | `java/middleware/registry-middleware/auth0` | `java/middleware/registry-middleware/generic-iam` |
| Provider class | `dev.sunbirdrc.auth.keycloak.KeycloakProviderImpl` | —                                           | `dev.sunbirdrc.auth.genericiam.AuthProviderImpl`  |

To support a different platform, take one of two paths.

:::::: tabs
== Build a submodule

:::: steps
::: step
#### Create the submodule

Under `java/middleware/registry-middleware`.
:::

::: step
#### Implement IdentityProvider

Implement the [`IdentityProvider`](https://github.com/Sunbird-RC/sunbird-rc-core/blob/generic-auth/java/middleware/registry-middleware/identity-provider/src/main/java/dev/sunbirdrc/registry/identity_providers/providers/IdentityProvider.java) interface (returns an `IdentityManager`); see the [Keycloak implementation](https://github.com/Sunbird-RC/sunbird-rc-core/blob/generic-auth/java/middleware/registry-middleware/keycloak/src/main/java/dev/sunbirdrc/auth/keycloak/KeycloakProviderImpl.java) as an example.
:::

::: step
#### Implement IdentityManager

[`IdentityManager`](https://github.com/Sunbird-RC/sunbird-rc-core/blob/generic-auth/java/middleware/registry-middleware/identity-provider/src/main/java/dev/sunbirdrc/registry/identity_providers/pojos/IdentityManager.java) handles user creation and returns the user id.
:::

::: step
#### Register as a Service Provider

Under `META-INF/services` — file name is the fully-qualified SPI name, contents are the fully-qualified implementation name.
:::

::: step
#### Point the registry at it

Set `identity_provider` to your new implementation's package name.
:::
::::

== Build an external wrapper

Skip the submodule and build an external wrapper service exposing an API to create users in your IAM platform, following [this API spec](https://github.com/Sunbird-RC/sunbird-rc-core/blob/6a99ab9d564ef0518ff5fa8f6730a58e51808f6d/services/sample-fusionauth-service/api-spec.yml). A [sample FusionAuth implementation](https://github.com/Sunbird-RC/sunbird-rc-core/tree/6a99ab9d564ef0518ff5fa8f6730a58e51808f6d/services/sample-fusionauth-service) is provided.

::: info
Both links are pinned to a historical commit — the `services/` directory has since evolved, but the commit links still resolve.
:::

Then set:

```bash
identity_provider=dev.sunbirdrc.auth.genericiam.AuthProviderImpl
sunbird_sso_url=http://localhost:8080/auth/   # replace with your service endpoint
```
::::::

