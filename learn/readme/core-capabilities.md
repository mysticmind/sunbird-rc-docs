---
title: "Core Capabilities"
description: "What Sunbird RC can do out of the box — with Registry and Credentials, used on their own or together."
---

# Core Capabilities

What Sunbird RC can do out of the box — with Registry and Credentials, used on their own or together.

<figure><img src="/images/core-3c5bce15.png" alt=""><figcaption></figcaption></figure>

Sunbird RC is one open-source package with two components, **Registry** and **Credentials**. You can use either one on its own, or both together. This page lists what each component can do and the status of each capability.

## Capability matrix

Status labels follow the [Roadmap](/help/roadmap): **Released**, **Experimental**, **In Development** and **Roadmap**.

| Component              | Capability                                                                                            | Status            |
| ---------------------- | ----------------------------------------------------------------------------------------------------- | ----------------- |
| Registry               | Schema definition, with field types and field-level privacy                                           | Released          |
| Registry               | Entity creation: bulk onboarding via CSV, self-registration, links to external systems                | Released          |
| Registry               | Ownership, login and authorization                                                                    | Released          |
| Registry               | Discovery with public, private and consent-based visibility                                           | Released          |
| Registry               | Attestation and claim workflows                                                                       | Released          |
| Registry               | Consent: grant, revoke and audit access                                                               | Released          |
| Registry               | Basic analytics                                                                                       | Released          |
| Credentials            | W3C-compliant credential issuance, update and revocation                                              | Released          |
| Credentials            | Credential formats: `ldp_vc`, `jwt_vc_json`, `vc+sd-jwt`, `mso_mdoc`                                  | Released          |
| Credentials            | Wallet issuance via OpenID4VCI 1.0 (draft-13 compatible)                                              | Released (opt-in) |
| Credentials            | Wallet presentation via OpenID4VP 1.0 (draft-23)                                                      | Released (opt-in) |
| Registry + Credentials | [Authority Service](#authority-service): multi-tenant access control, configuration and record review | In Development    |

## Registry

A governing body or authority can build a registry that acts as a **single source of truth**.

1. **Define schema as per policy**
   * **Fields and field types:** Create new fields in the registry to store specific types of information, and specify the type of data each field accepts. For example, a student registry might define fields for student name, father's name, mother's name, school name and age — with the age field accepting only numbers.
   * **Field-level privacy:** Set different levels of privacy for different fields based on how sensitive their data is. For example, in a patient registry, fields containing health information can be restricted to authorized healthcare professionals, while less sensitive fields such as demographics are available to a wider range of users.
   * **Consent framework** at schema level
2. **Create entities**
   * Bulk invite or onboard users via CSV
   * Link to external systems
   * Let users self-register
   * Decide, at field level, who can view the content
3. **Define ownership**
   * Define which entities can log in and how authorization is handled
4. **Discovery**
   * Control the visibility of discovery attributes through access control mechanisms such as consent-based sharing. Users can mark each discovery attribute as **public** (visible to all users), **private** (visible only to the user) or **consent-based** (visible to selected users or groups based on their consent).
5. **Attestation and claim workflows**
   * Tenants (users) can define an add-on workflow, customizing its steps to suit their needs, and configure whether claims are approved automatically or manually.
   * Attestation can run on an internal system like Sunbird RC, or on an external system the tenant connects to.
   * Claims can go through multi-level attestation — reviewed by multiple parties or levels of approval.
   * Define validity
6. **Consent**
   * **Grant or revoke consent:** Receive consent requests and grant or revoke access.
   * Consent auditing
7. **Analytics**
   * Basic analytics for registries

## Credentials

1. **Issuance services**
   * W3C compliant
   * Create and issue verifiable credentials
   * Update and revoke credentials
   * Unique ID generation
2. **Verification**
   * Anyone can verify a credential's signature and status.
   * Holders share credentials with a verifier by consent, from their own wallet.
3. **Digital wallet interoperability (opt-in)**
   * Credentials implements OpenID4VCI and OpenID4VP through the OID4VC service, so citizens can use **any compliant wallet** — Sunbird-built or third-party — to hold and present their credentials. The OID4VC service is optional and is enabled separately.

:::: tabs
== Fetch and store credentials

* **Issuance via OpenID4VCI 1.0** (draft-13 compatible): the issuer publishes a credential offer, the wallet resolves it, exchanges a pre-authorized code for a token, then proves key possession (nonce + PoP) to fetch the credential.
* Supports deferred issuance and issuance notifications.
* **Formats:** `ldp_vc`, `jwt_vc_json`, `vc+sd-jwt`, `mso_mdoc`
* Standard `.well-known` discovery endpoints — no custom wallet integration needed.

== Share with consent

* **Presentation via OpenID4VP 1.0** (draft-23): the verifier describes the claims it needs via DCQL, and the wallet fetches the request object and returns a `vp_token`.
* **Consent is enforced at the wallet** — the holder decides what to disclose against the query; there is no blanket handover.
* The verifier polls the presentation status to confirm what was shared.
::::

## Using Registry and Credentials together

When both components are deployed, a registry can issue verifiable credentials from its own records. Registry's signing and DID features (Signature V2) are provided by the Credentials services, and the registry can also hand credentials to wallets through the OID4VC service.

## In development

### Authority Service

::: warning
**In Development.** The Authority Service is not part of any Sunbird RC release yet. Its design, APIs and behaviour may change. Don't use it in production.
:::

**What it is.** The Authority Service is a small, reusable, **domain-neutral** administrative layer that sits in front of Sunbird RC. It provides multi-tenant access control, configuration, and a lightweight record-review workflow for any registry entity — without encoding business logic specific to a particular sector (agriculture, education, etc.).

**Why it exists.** Sunbird RC already supports per-record ownership, login, field-level privacy, consent and attestation workflows. What it doesn't provide is **multi-tenancy**: a way for each organisation's administrators able to manage only their own registries and records. The Authority Service adds that layer, so multiple organisations can share one instance safely, with a basic review step before a record is treated as trustworthy.

**Core model.**

```
Authority → Registry → Credential Profile → Credential
```

Definitions of each level, and how they map to existing Sunbird RC concepts such as registry schemas and credential schemas, will be added here.

**Where it fits.** The Authority Service sits in front of Sunbird RC and works across both components. Whether it is optional, and how it is used alongside direct calls to the Registry and Credentials APIs, is being confirmed.

**Status and scope.** Not included in any release. The target release and first-release scope are being confirmed — see the [Roadmap](/help/roadmap). Follow progress on [GitHub Discussions](https://github.com/orgs/Sunbird-RC/discussions).

## Core Registry Verbs

<figure><img src="/images/image-c529abba.png" alt=""><figcaption></figcaption></figure>
