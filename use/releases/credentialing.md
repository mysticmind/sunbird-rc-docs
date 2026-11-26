---
title: "Credentialling"
---

# Credentialling

Release history for the Credentialling Services — Identity, Credential Schema, and Credential.

## v2.1.0 — Standards-based wallet interoperability <a href="#v2.1.0" id="v2.1.0"></a>

<p class="update-meta">2026-08-10 · new release, improvements</p>

::: card
[v2.1.0 — Latest release](/use/releases/credentialing/v2.1.0-latest-release)
:::

The first feature-bearing release in roughly two years. A new `oid4vc-service` makes the platform speak **OpenID4VCI 1.0** for issuance and **OpenID4VP 1.0/draft-23** for presentation, so any conformant wallet can receive a credential from a Sunbird RC deployment and present it back to a Sunbird RC verifier with no Sunbird-specific integration. Four credential formats are supported end-to-end, and W3C VC Data Model 2.0 lands alongside the existing 1.1 support.

Read the full v2.1.0 release notes

---

## v2.0.3 — Security and stability <a href="#v2.0.3" id="v2.0.3"></a>

<p class="update-meta">2026-05-21 · fixes</p>

::: card
[v2.0.3](/use/releases/credentialing/v2.0.3)
:::

The platform-wide maintenance release, as it applied to the credentialling stack: Node dependency remediation across the Credential, Credential Schema and Identity services, the same hardened image baseline, and the repository-wide secrets cleanup.

---

## v2.0.0-beta3 — Initial Credentialling Services release <a href="#v2.0.0-beta3" id="v2.0.0-beta3"></a>

<p class="update-meta">2024-02-13 · improvements</p>

::: card
[v2.0.0](/use/releases/credentialing/v2.0.0)
:::

The first release of the three-service credentialling stack — Identity Service, Credential Schema Service and Credential Service — which replaced the registry's older built-in signing and certificate path.

---

***

## Artifacts

All images are published on GHCR.

| Artifact                  | Image                                              |
| ------------------------- | -------------------------------------------------- |
| Identity Service          | `ghcr.io/sunbird-rc/sunbird-rc-identity-service`   |
| Credential Schema Service | `ghcr.io/sunbird-rc/sunbird-rc-credential-schema`  |
| Credential Service        | `ghcr.io/sunbird-rc/sunbird-rc-credential-service` |
