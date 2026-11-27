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

```mermaid
flowchart TB
    Ingress[Ingress]
    subgraph Core["Core credentialling services"]
        OID4VC[oid4vc-service]
        Creds[Credentials service]
        Identity[Identity service]
        Schema[Credential schema service]
    end
    subgraph Aux["Auxiliary services"]
        Vault[HashiCorp Vault]
        Redis[Redis]
    end
    IssuanceDB[(Credential issuance DB)]
    IdentityDB[(Identity service DB)]
    SchemaDB[(Credential schema DB)]

    Ingress --> OID4VC
    Ingress --> Creds
    Ingress --> Identity
    Ingress --> Schema
    OID4VC --> Creds
    OID4VC --> Identity
    OID4VC --> Schema
    OID4VC --> Redis
    Creds --> Identity
    Creds --> IssuanceDB
    Identity --> Schema
    Identity --> Vault
    Identity --> IdentityDB
    Schema --> SchemaDB

    classDef ingress fill:#fcd9d9,stroke:#c0504d,color:#1d1d1f
    classDef core fill:#dbe8f6,stroke:#4a7bab,color:#1d1d1f
    classDef aux fill:#d9f2d9,stroke:#3f8f3f,color:#1d1d1f
    classDef db fill:#fbeaa5,stroke:#b8962e,color:#1d1d1f
    class Ingress ingress
    class OID4VC,Creds,Identity,Schema core
    class Vault,Redis aux
    class IssuanceDB,IdentityDB,SchemaDB db
```

<p class="rc-legend"><span><i class="rc-swatch ingress"></i>Entry point</span><span><i class="rc-swatch core"></i>Core credentialling services</span><span><i class="rc-swatch scale"></i>Auxiliary services</span><span><i class="rc-swatch db"></i>Databases</span></p>

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

