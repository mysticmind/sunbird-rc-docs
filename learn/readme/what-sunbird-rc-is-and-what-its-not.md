---
title: "What Sunbird RC is and what it's not?"
description: "Where Sunbird RC fits — and what you'll still need to build or bring yourself."
---

# What Sunbird RC is and what it's not?

Where Sunbird RC fits — and what you'll still need to build or bring yourself.

Sunbird RC is a set of open-source building blocks for registries and verifiable credentials. This page draws the line clearly, so adopters know what they're getting and what they still need to build or bring themselves.

::: info
Sunbird RC is one open-source package with two components, **Registry** and **Credentials**. You can use either one on its own, or both together. Each component has its own release line and version number.
:::

## What Sunbird RC is

One open-source package with two components. You can use either one on its own, or both together. Each is made up of independently deployable microservices:

* **Registry** — a configurable, low-code registry: Registry (core), Claims / Attestation, Notification, Metrics, Encryption and ID Gen.
* **Credentials** — a W3C-compliant credentialing service: Identity, Credential Schema, Credential Issuance and OID4VC.

When both are used together, Registry's signing and DID features (Signature V2) are provided by the Credentials services.

For the full picture, see [Sunbird RC Overview](/learn/readme), Why do we need Sunbird RC? and Core Capabilities.

::: tip
**Works with any compliant wallet.** Through the OID4VC microservice, Sunbird RC now speaks OpenID4VCI (issuance) and OpenID4VP (presentation), so any compliant wallet — not just a Sunbird-built one — can fetch, hold and present credentials issued by the platform.
:::

## What Sunbird RC is not

<table data-search="false"><thead><tr><th width="220">Sunbird RC is not…</th><th>What that means for you</th></tr></thead><tbody><tr><td><strong>A wallet app</strong></td><td>Sunbird RC does not ship a holder-facing wallet with its own credential storage or UI — earlier wallet and verifier-app prototypes were removed from the codebase in favor of standards compliance. Citizens use any OpenID4VCI/VP-compliant wallet of their choice.</td></tr><tr><td><strong>An identity provider</strong></td><td>Authentication and authorization run through Keycloak by default, but Sunbird RC can sit behind any OpenID Connect-compliant IDP and OAuth2 resource server — it doesn't replace one.</td></tr><tr><td><strong>A consent management platform</strong></td><td>By design, the consent decision and disclosure happen inside the holder's own wallet — the verifier states what it needs via DCQL, and the wallet decides what to share. This keeps consent under the holder's control rather than logged on a central server.</td></tr><tr><td><strong>A blockchain or DID network</strong></td><td>DIDs are generated and resolved as part of identity management, but Sunbird RC doesn't operate a distributed ledger or implement DIDComm — it's a centrally operated registry with DID-compliant, web-resolvable identifiers.</td></tr><tr><td><strong>A turnkey vertical solution</strong></td><td>There's no built-in student registry, national ID system or health registry out of the box — every deployment defines its own schemas, workflows and attestation policy to fit its use case.</td></tr></tbody></table>
