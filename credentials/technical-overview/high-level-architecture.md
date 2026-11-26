---
title: "High-Level Architecture"
description: "The microservices behind Sunbird RC credentialling, and how identity, schema, issuance and verification flows work."
---

# High-Level Architecture

The microservices behind Sunbird RC credentialling, and how identity, schema, issuance and verification flows work.

Sunbird RC's credentialling service is made up of three microservices. Expand each to learn what it does.

<details>

<summary>Identity microservice</summary>

The central lynchpin for maintaining identities across the system. All identities in Sunbird RC are DID-compliant and web-resolvable. The other two microservices (Credential Schema and Credential Issuance) depend on it to generate any identity.

</details>

<details>

<summary>Credential Schema microservice</summary>

Stores the schema of each verifiable credential, along with its associated view template.

</details>

<details>

<summary>Credential Issuance microservice</summary>

The core issuance service. It takes a payload, transforms it into a W3C-compliant verifiable credential in JSON-LD format, and signs it using the private key generated when the issuer was created.

</details>

## High-level component diagram

<figure><img src="/images/component-85b96f5b.png" alt=""><figcaption></figcaption></figure>

## How it works

:::: tabs
== Direct API flow

This sequence diagram explains the following flows:

* Creating an identity
* Creating a schema
* Issuing a credential
* Verifying a credential

<figure><img src="/images/credential-sequence-1-4c1b8440.png" alt=""><figcaption></figcaption></figure>

== OID4VC / VP wallet flow

This sequence diagram explains the OID4VC/VP flow:

* Creating an identity
* Creating a schema
* Fetching issuer metadata (OID4VCI discovery)
* Issuing a credential (OID4VCI, wallet-initiated pre-authorized flow)
* Verifying a credential (OID4VP, DCQL-based presentation)

<figure><img src="/images/sequence-diagram-oid4vc-51eb5717.png" alt=""><figcaption></figcaption></figure>
::::

