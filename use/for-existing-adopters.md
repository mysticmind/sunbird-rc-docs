---
title: "For existing adopters"
description: "What's new, what changed, and how to upgrade an existing Sunbird RC deployment."
---

# For existing adopters

What's new, what changed, and how to upgrade an existing Sunbird RC deployment.

Already running Sunbird RC? This page brings together what you need before moving to a newer release: what's new, what changed, what stays compatible, and how to upgrade.

::: info
**This page is being completed.** Some compatibility details are still being confirmed with the RC team. Rows marked **Being confirmed** are incomplete — check the release notes and ask on [GitHub Discussions](https://github.com/orgs/Sunbird-RC/discussions) before relying on them.
:::

## What's new

**v2.1.0** adds the **OID4VC service**, which lets any standards-compliant wallet receive credentials through OpenID4VCI 1.0 and present them through OpenID4VP 1.0 (draft-23). The service is **opt-in**: it only runs when you enable the `oid4vc` profile, so an existing deployment keeps working as before until you turn it on.

The release also updates the runtime and dependencies of every service in the repository.

* [v2.1.0 release notes](/use/releases/credentialing/v2.1.0-latest-release)
* [Wallet Integration](/use/integrations/wallet-integration) — how the OID4VC service works with wallets

## What changed from v1 to v2

The biggest change between major versions is how the Registry signs credentials. From v2, the Registry can use either the legacy signer (Signature V1) or the Credentials services (Signature V2). You choose with the `signature_provider` setting.

|                      | Signature V1 (v1 and older)                                                     | Signature V2                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Signing keys**     | Created manually and placed in a config file before deploying                   | Created by the identity service when an issuer is created; the private key is held in HashiCorp Vault                           |
| **Adding a key**     | Add it to the file manually and redeploy                                        | Keys are created as needed                                                                                                      |
| **Signature suites** | `RsaSignature2018`                                                              | `Ed25519Signature2020`, `Ed25519Signature2018`, `RsaSignature2018`                                                              |
| **Services needed**  | certificate-signer, certificate-api                                             | identity, credential-schema, credentials, Vault                                                                                 |
| **Setting**          | `signature_provider=dev.sunbirdrc.registry.service.impl.SignatureV1ServiceImpl` | `signature_provider=dev.sunbirdrc.registry.service.impl.SignatureV2ServiceImpl`, plus the `did_*` and `signature_v2_*` settings |

For more on each option, see [Signature V1 or V2](/use/developer-guide/working-with-source-code#signature-v1-or-v2).

## Compatibility

| Area                           | What changes                                                                                                                                            | Status          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **Registry APIs**              | From v2, the list-entity and search APIs are paginated and return a different response structure from v1. Update any client that reads these responses. | Documented      |
| **Registry schemas**           | Schema versioning isn't supported. Adding or removing fields has to be managed outside Sunbird RC.                                                      | Documented      |
| **Keys and DIDs**              | After switching from Signature V1 to V2, new credentials are signed with keys held in Vault and use V2 DIDs.                                            | Documented      |
| **Credentials already issued** | Whether credentials issued under V1 can still be verified after switching to V2.                                                                        | Being confirmed |
| **Data**                       | Whether existing registry data needs migrating between releases.                                                                                        | Being confirmed |
| **Credential schemas**         | Whether existing credential schemas need changes between releases.                                                                                      | Being confirmed |
| **Deployment configuration**   | Which environment variables and settings change between releases.                                                                                       | Being confirmed |

## Upgrade steps (Docker Compose)

::::: steps
::: step
### Read the release notes

Check the release notes for every version between yours and the one you're moving to. See [Previous versions](#previous-versions) below.
:::

::: step
### Back up your data

Back up your databases before upgrading. See [Backup and Restore](/use/developer-guide/backup-and-restore).
:::

::: step
### Update the release version

In your `.env` file, set `RELEASE_VERSION` to the new release tag, for example `v2.1.0`. Then pull the new images and restart:

```bash
docker compose pull
docker compose up -d
```
:::

::: step
### Optional: enable the OID4VC service

```bash
docker compose --profile oid4vc up -d oid4vc-service
```

See [Wallet Integration](/use/integrations/wallet-integration) for the settings it needs.
:::

:::: step
### Optional: switch from Signature V1 to V2

From the `sunbird-rc-core` folder, run:

```bash
bash enable-v2.sh
```

This brings up Vault, identity, credential-schema, credentials and claim-ms, and restarts the Registry with signing, DIDs and claims turned on.

::: warning
Switching changes how new credentials are signed and which DIDs they use. Check the impact on credentials you have already issued before switching.
:::
::::
:::::

::: info
**Upgrading a Helm deployment?** Helm upgrade steps are being confirmed and will be added here.
:::

## Previous versions

**Registry**

* [v2.0.3](/use/releases/registry/v2.0.3)
* [v1.0.0](/use/releases/registry/v1.0.0)

**Credentials**

* [v2.1.0](/use/releases/credentialing/v2.1.0-latest-release)
* [v2.0.3](/use/releases/credentialing/v2.0.3)
* [v2.0.0](/use/releases/credentialing/v2.0.0)

All releases and changelogs are also on [GitHub](https://github.com/Sunbird-RC/sunbird-rc-core/releases).
