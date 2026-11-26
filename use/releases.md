---
title: "Releases"
---

# Releases

## Latest release — v2.1.0

**Released 10 August 2026** · Tagged `v2.1.0`

v2.1.0 is the first feature-bearing release of Sunbird RC in roughly two years — the last was v2.0.2 in August 2024, with v2.0.3 a maintenance release in between. It is both a major feature release and a platform-wide upgrade: every service in the repository has been touched, either to add the new capability or to bring its runtime and dependency tree up to date.

The headline is **OpenID Connect for Verifiable Credentials**. A new `oid4vc-service` makes the platform speak OpenID4VCI 1.0 for issuance and OpenID4VP 1.0/draft-23 for presentation, so any conformant wallet can receive a credential from a Sunbird RC deployment and present it back to a Sunbird RC verifier — with no Sunbird-specific integration on the wallet side.

::: card
[v2.1.0 — Latest release](/use/releases/credentialing/v2.1.0-latest-release)
:::

::: info
**Checkout other** <a href="https://github.com/orgs/Sunbird-RC/packages?repo_name=sunbird-rc-core" class="button primary small" data-icon="box-isometric">Releases & Changelogs</a>
:::

