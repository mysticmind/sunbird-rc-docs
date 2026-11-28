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

```mermaid
sequenceDiagram
    autonumber
    actor Caller as Calling System
    participant Identity as Identity Service
    participant Schema as Credential Schema
    participant Issuance as Credential Issuance Service
    participant Vault as Hashicorp Vault
    participant DB as Database

    loop Creating an Issuer Identity
        Caller->>+Identity: Create an Identity<br/>for the Issuer
        Identity->>Identity: Generate Public and Private Key<br/>for an identity
        Identity-->>Vault: Persist the Key Pair<br/>into the vault
        Identity-->>DB: Persist into the database
        Identity-->>-Caller: Returns a DID compliant<br/>Identity
        Note over Caller,Identity: The DID document contains<br/>Identity metadata with<br/>the associated public key
    end

    loop Creating a credential Schema and template for presentation
        Caller->>+Schema: Create Schema
        Schema->>+Identity: Create an identity<br/>for the schema
        Identity->>Identity: Generate a Key Pair
        Identity-->>Vault: Persist Key Pair to Vault
        Identity-->DB: Persist Identity in database
        Identity-->>-Schema: Return DID compliant Identifier
        Schema-->DB: Persist Schema into Database
        Schema-->>-Caller: Return schema Identifier
        Caller->>+Schema: Add template to schema
        Schema-->>DB: Add Template to Schema
        Schema-->>-Caller: Return status
        Note over Caller,Schema: Credential Schema creation is mandatory for Credential Issuance.<br/>The payload for the credential is validated against the credential schema.<br/>The payload is transformed into the View Template.
    end

    loop Generating a Verifiable Credential
        Caller->>+Issuance: Request to Issue a credential
        Issuance-->>+Schema: Request to Retrieve associated credential schema
        Schema-->>-Issuance: Retrieve associated schema
        Issuance->>+Identity: Request Issuer Identity
        Identity->>+Vault: Request Keys for Issuer
        Vault->>-Identity: Retrieve Keys for Issuer
        Identity-->>-Issuance: Retrieve Issuer DID with Keys
        Issuance->>Issuance: Validate payload against Schema<br/>and convert to JSON-LD W3C-VC data model
        Issuance->>Issuance: Sign payload and add proof
        Issuance-->>-Caller: Issue W3C compliant Verifiable Credentials
    end

    loop Verify a Sunbird-RC issued Verifiable Credential
        Caller->>+Issuance: Request to verify a Verifiable Credential
        Issuance->>+Identity: Request to retrieve the DID document for the issuer
        Identity-->>Vault: Retrieve public Key of the Issuer
        Identity-->>-Issuance: DID Document of the issuer including the public key
        Issuance->>Issuance: Validate the proof section of the VC<br/>using Issuer's public key
        Issuance->>Issuance: Validate against revocation list
        Issuance-->>-Caller: Respond with the Verification status
    end
```

== OID4VC / VP wallet flow

This sequence diagram explains the OID4VC/VP flow:

* Creating an identity
* Creating a schema
* Fetching issuer metadata (OID4VCI discovery)
* Issuing a credential (OID4VCI, wallet-initiated pre-authorized flow)
* Verifying a credential (OID4VP, DCQL-based presentation)

```mermaid
sequenceDiagram
    autonumber
    actor Caller as Calling System<br/>(Issuer/Verifier)
    participant Wallet
    participant Identity as Identity Service
    participant Schema as Credential Schema
    participant Creds as Credentials Service
    participant OID4VC as OID4VC Service
    participant Vault as Hashicorp Vault
    participant Database@{ "type" : "database" }

    loop Creating an Issuer Identity
        Caller->>+Identity: Create an Identity<br/>for the Issuer
        Identity->>Identity: Generate Public and Private Key<br/>for an identity
        Identity-->>Vault: Persist the Key Pair<br/>into the vault
        Identity-->>Database: Persist into the database
        Identity-->>-Caller: Returns a DID compliant<br/>Identity
    end

    loop Creating a credential Schema with OID4VCI config
        Caller->>+Schema: Create Schema<br/>(formats, vct, display, mdoc config)
        Schema->>+Identity: Create an identity<br/>for the schema author
        Identity->>Identity: Generate a Key Pair
        Identity-->>Vault: Persist Key Pair to Vault
        Identity-->>Database: Persist Identity in database
        Identity-->>-Schema: Return DID compliant Identifier
        Schema-->>Database: Persist Schema + oid4vciConfig into Database
        Schema-->>-Caller: Return schema Identifier
    end
    Note over Caller,Schema: oid4vciConfig (formats, vct, mdoc docType/namespace,<br/>renderMethod) drives what OID4VC Service later<br/>publishes in its issuer metadata.

    Note over Caller,Database: OID4VCI: Credential Issuance
    Wallet->>+OID4VC: GET /oid4vc/.well-known/openid-credential-issuer
    OID4VC->>+Schema: Request OID4VCI-enabled<br/>schema configs
    Schema-->>-OID4VC: Return schema configs<br/>(formats, vct, display)
    OID4VC-->>-Wallet: credential_configurations_supported

    loop Generating a Verifiable Credential
        Caller->>+OID4VC: POST /oid4vc/offer<br/>(credential_configuration_id, claims)
        OID4VC->>+Schema: Resolve credential config<br/>by schemaId
        Schema-->>-OID4VC: Return config + issuer DID
        OID4VC->>OID4VC: Create offer session<br/>(pre-authorized_code)
        OID4VC-->>-Caller: credential_offer_uri / qr_data
        Caller-->>Wallet: Present offer QR / deep link
        Wallet->>+OID4VC: GET /oid4vc/offer/:id
        OID4VC-->>-Wallet: credential_offer<br/>(grants: pre-authorized_code)
        Wallet->>+OID4VC: POST /oid4vc/token<br/>(pre-authorized_code)
        OID4VC->>OID4VC: Validate + consume code,<br/>mint access_token + c_nonce
        OID4VC-->>-Wallet: access_token, c_nonce
        Wallet->>Wallet: Generate key pair,<br/>build proof-of-possession JWT (c_nonce)
        Wallet->>+OID4VC: POST /oid4vc/credential<br/>(access_token, proof.jwt)
        OID4VC->>OID4VC: Verify PoP proof + nonce
        OID4VC->>+Creds: Request to issue credential<br/>(claims, schemaId, format, holder key)
        Creds->>+Identity: Request Issuer Identity / Keys
        Identity->>+Vault: Request Keys for Issuer
        Vault->>-Identity: Retrieve Keys for Issuer
        Identity-->>-Creds: Retrieve Issuer DID with Keys
        Creds->>Creds: Validate payload against Schema<br/>and convert to JSON-LD / SD-JWT / mdoc
        Creds->>Creds: Sign payload and add proof<br/>(binds holder key via cnf)
        Creds-->>-OID4VC: Signed Verifiable Credential
        OID4VC-->>-Wallet: Issue W3C / SD-JWT / mdoc<br/>Verifiable Credential + new c_nonce
    end
    Note over Wallet,OID4VC: Deferred issuance: if the credential is not yet ready,<br/>/oid4vc/credential returns a transaction_id instead#59; the<br/>Wallet polls POST /oid4vc/deferred until issuance completes.

    Note over Caller,Database: OID4VP: Credential Presentation
    loop Verify a Sunbird-RC issued Verifiable Credential
        Caller->>+OID4VC: POST /vp/request<br/>(dcql_query)
        OID4VC->>+Identity: Sign request object (JAR)<br/>with verifier DID
        Identity-->>-OID4VC: Signed JWS
        OID4VC->>OID4VC: Create VP transaction<br/>(nonce, state)
        OID4VC-->>-Caller: transaction_id, request_uri, qr_data
        Caller-->>Wallet: Present verification QR / deep link
        Wallet->>+OID4VC: GET /vp/request-object/:id
        OID4VC-->>-Wallet: Signed/unsigned request object<br/>(dcql_query)
        Wallet->>Wallet: Select matching credential(s),<br/>build vp_token + holder binding proof
        Wallet->>+OID4VC: POST /vp/response<br/>(vp_token, state)
        OID4VC->>OID4VC: Validate client_id/response_uri,<br/>nonce, audience
        OID4VC->>+Creds: Verify embedded credential(s)<br/>(signature, revocation, holder binding)
        Creds->>+Identity: Resolve Issuer DID Document<br/>/ public key
        Identity-->>-Creds: DID Document with public key
        Creds->>Creds: Validate proof against<br/>Issuer's public key
        Creds->>Creds: Validate against revocation list
        Creds-->>-OID4VC: Verification checks result
        OID4VC->>OID4VC: Evaluate DCQL match,<br/>store verified result
        OID4VC-->>-Wallet: status: ok
        Caller->>+OID4VC: GET /vp/status/:id
        OID4VC-->>-Caller: Verification status + disclosed claims
    end
```
::::

