---
title: "Registry"
---

# Registry

Release history for the Sunbird RC core registry.

## v2.0.3 — Security and stability <a href="#v2.0.3" id="v2.0.3"></a>

<p class="update-meta">2026-05-21 · fixes, improvements</p>

A maintenance release: CVE remediation and platform hardening across all core services, with no new capability. Java and Spring dependencies moved onto patched versions, service images were rebuilt on Eclipse Temurin 11 as non-root with pinned tags and healthchecks, committed secrets were purged from the repository, and three concurrency fixes landed in the registry itself.

::: card
[v2.0.3](/use/releases/registry/v2.0.3)
:::

---

## v1.0.0 — OAuth2 everywhere, field-level encryption, functional identifiers <a href="#v1.0.0" id="v1.0.0"></a>

<p class="update-meta">2023-11-15 · improvements</p>

The release that decoupled Sunbird RC from Keycloak — any OAuth2/OIDC-compliant provider can now serve as the identity layer. Also introduced field-level encryption and masking for private fields, functional identifier generation via DIGIT Id-Gen, Registry CLI enhancements, and the migration of platform images from Docker Hub to GHCR.

::: card
[v1.0.0](/use/releases/registry/v1.0.0)
:::

---

## v0.0.14 <a href="/v0.0.14/use/releases" class="button secondary small" data-icon="gitbook">Checkout the v0.0.14 Release Notes</a> <a href="#v0.0.14" id="v0.0.14"></a>

<p class="update-meta">2023-06-30</p>

See the release notes on Gitbook for the details of this release.

---

***

## Artifacts

All images are published on GHCR. `latest` always points to the newest platform version, which is also tagged explicitly on the image.

| Artifact                    | Image                                                      |
| --------------------------- | ---------------------------------------------------------- |
| Sunbird-RC Core             | `ghcr.io/sunbird-rc/sunbird-rc-core`                       |
| Claims services             | `ghcr.io/sunbird-rc/sunbird-rc-claims-ms`                  |
| Certificate Signer services | `ghcr.io/sunbird-rc/sunbird-rc-certificate-signer`         |
| Certificate services        | `ghcr.io/sunbird-rc/sunbird-rc-certificate-api`            |
| Notification services       | `ghcr.io/sunbird-rc/sunbird-rc-notification-service`       |
| Digilocker services         | `ghcr.io/sunbird-rc/sunbird-rc-digilocker-certificate-api` |
| Metrics services            | `ghcr.io/sunbird-rc/sunbird-rc-metrics`                    |
| Bulk issuance services      | `ghcr.io/sunbird-rc/sunbird-rc-bulk-issuance`              |
| Public Key services         | `ghcr.io/sunbird-rc/sunbird-rc-public-key-service`         |
| Context Proxy services      | `ghcr.io/sunbird-rc/sunbird-rc-context-proxy-service`      |
| Keycloak                    | `ghcr.io/sunbird-rc/sunbird-rc-keycloak`                   |
| ID Generation services      | `ghcr.io/sunbird-rc/id-gen-service`                        |
| Encryption services         | `ghcr.io/sunbird-rc/encryption-service`                    |

::: warning
Per the Custom QR Code and LEARN-section audit findings, `certificate-signer` and `certificate-api` images may be deprecated/renamed — confirm against the current [Sunbird-RC package registry](https://github.com/orgs/Sunbird-RC/packages?repo_name=sunbird-rc-core) before relying on these image names.
:::

