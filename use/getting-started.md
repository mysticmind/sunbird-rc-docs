---
title: "Getting started"
---

# Getting started

Sunbird RC is one open-source package with two components, **Registry** and **Credentials**. You can use either one on its own, or both together. Pick the path that matches what you need.

## New to Sunbird RC? Choose your path

| Path                       | Choose this if you want to…                                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| **Registry only**          | Build an authoritative registry of people, entities or things, with APIs, attestation and consent. |
| **Credentials only**       | Issue and verify W3C verifiable credentials from data you already hold in another system.          |
| **Registry + Credentials** | Build a registry and issue verifiable credentials from its records.                                |

Before you start, install the [Pre-requisites](/use/getting-started/developer-setup) for your path.

:::: tabs
== Registry only

**Quick start**

* [Docker Compose Setup](/use/getting-started/installation/docker-compose-setup) — the default settings leave credential signing off, so the Registry runs on its own.
* Or the [Registry CLI](/use/getting-started/installation/registry-cli) for a guided local setup.

**Next steps**

* [Creating Your Own Schemas](/use/developer-guide/schema-setup/creating-your-own-schemas)
* [Registry API reference](/registry/api-reference/registry/using-the-apis)
* [Core Capabilities](/learn/readme/core-capabilities)

== Credentials only

**Quick start**

* [Credentialling Services setup](/use/getting-started/installation/credentialling-services-setup-dev-docker-helm) — use the **Docker Compose** tab.

**Next steps**

* [Credentials API reference](/credentials/api-reference/credential-issuance-apis)
* [Wallet Integration](/use/integrations/wallet-integration) — optional, to issue to and verify from any compliant wallet

== Registry + Credentials

**Quick start**

1. Follow [Docker Compose Setup](/use/getting-started/installation/docker-compose-setup).
2. From the `sunbird-rc-core` folder, run `bash enable-v2.sh`. This brings up Vault, identity, credential-schema, credentials and claim-ms, and restarts the Registry with signing, DIDs and claims turned on.

**Next steps**

* [Signature V1 or V2](/use/developer-guide/working-with-source-code#signature-v1-or-v2) — how the Registry signs credentials
* [Wallet Integration](/use/integrations/wallet-integration) — optional
::::

## Going to production

For a Kubernetes deployment, see [Helm Setup](/use/getting-started/installation/helm-setup) and the **Helm** tab of [Credentialling Services setup](/use/getting-started/installation/credentialling-services-setup-dev-docker-helm).

::: warning
The production deployment guides are being reviewed for v2.1.0. Check with the community on [GitHub Discussions](https://github.com/orgs/Sunbird-RC/discussions) before deploying to production.
:::

## Already running Sunbird RC?

See [For existing adopters](/use/getting-started/for-existing-adopters) for what's new, what changed, compatibility and upgrade steps.

## In this section

* [Pre-requisites](/use/getting-started/developer-setup)
* [Installation](/use/getting-started/installation)
* [For existing adopters](/use/getting-started/for-existing-adopters)
