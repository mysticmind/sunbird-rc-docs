---
title: "Technical Specification Draft"
description: "Data models, schemas, issuance, verification, revocation, DIDs and wallet protocols for Sunbird RC credentialling."
---

# Technical Specification Draft

Data models, schemas, issuance, verification, revocation, DIDs and wallet protocols for Sunbird RC credentialling.

::: info
**This is an early draft of the specification.** Help us improve it by sharing feedback in the [Discussions area](https://github.com/Sunbird-RC/community/discussions/categories/sunbird-rc-technical-specification-feedback).
:::

## Introduction

A **Verifiable Credential (VC)** is a digitally signed, tamper-evident statement issued by one party (the Issuer) about a subject, held by another (the Holder), and checked by a third (the Verifier) — without the verifier needing to call back the issuer online.

Sunbird RC's credentialing subsystem builds, signs, stores and verifies these credentials on top of registry data, and exposes standards-based protocols so any compliant wallet can fetch and present them.

## Core principles

<table data-search="false"><thead><tr><th width="200">Principle</th><th>What it means</th></tr></thead><tbody><tr><td><strong>Portable</strong></td><td>Once issued, a credential is controlled by its holder and can be carried, stored and presented independently of the issuer's systems.</td></tr><tr><td><strong>Tamper-evident</strong></td><td>Every credential is cryptographically signed by the issuer. Any modification after issuance invalidates the signature.</td></tr><tr><td><strong>Interoperable</strong></td><td>Issuance and verification run over open protocols (W3C VC Data Model, OpenID4VCI, OpenID4VP), so credentials from one deployment can be verified by any conformant party — not just other Sunbird RC instances.</td></tr></tbody></table>

## Terminology

<table data-search="false"><thead><tr><th width="262.05859375">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Issuer</strong></td><td>The entity that creates and digitally signs a credential.</td></tr><tr><td><strong>Holder</strong></td><td>The entity (usually the subject) that receives and stores a credential, typically in a wallet.</td></tr><tr><td><strong>Verifier</strong></td><td>The entity that checks a credential's or presentation's validity.</td></tr><tr><td><strong>Verifiable Credential (VC)</strong></td><td>A signed, machine-verifiable statement about a subject, per the W3C VC Data Model.</td></tr><tr><td><strong>Verifiable Presentation (VP)</strong></td><td>A holder-constructed, signed bundle of one or more credentials (or selected claims from them) shared with a verifier.</td></tr><tr><td><strong>DID</strong></td><td>Decentralized Identifier — a web-resolvable identifier used for issuers, and minted per-credential as the credential's own id.</td></tr><tr><td><strong>Proof</strong></td><td>The cryptographic signature block attached to a credential, binding it to the issuer's key.</td></tr><tr><td><strong>Credential Schema</strong></td><td>The JSON Schema defining a credential type's structure, stored and versioned in the Credential Schema service.</td></tr><tr><td><strong>Status List</strong></td><td>A bitstring-based revocation mechanism (RevocationList2020-style) — one bit per credential, one list per issuer.</td></tr><tr><td><strong>DCQL</strong></td><td>Digital Credentials Query Language — how a verifier describes which claims/credentials it needs in an OpenID4VP request.</td></tr></tbody></table>

## Data model versions

Sunbird RC issues and verifies credentials against both the **W3C VC Data Model 1.1** and **2.0** contexts:

<table><thead><tr><th width="160">Version</th><th>Validity fields</th></tr></thead><tbody><tr><td><strong>1.1</strong></td><td><code>issuanceDate</code> / <code>expirationDate</code></td></tr><tr><td><strong>2.0</strong></td><td><code>validFrom</code> / <code>validUntil</code></td></tr></tbody></table>

Both field sets are optional on the internal credential type, so either context validates.

::: tip
**Works offline.** The 2.0 context (`https://www.w3.org/ns/credentials/v2`) is bundled locally in both the Credential Issuance and Identity microservices, so 2.0 credentials sign and verify offline the same way 1.1 credentials already did — no network fetch of the context document at runtime.
:::

## Credential Schema

Schemas are stored as JSON documents combining metadata with an embedded JSON Schema for the credential subject. Example (`services/credential-schema/samples/proof_of_marks.json`, trimmed):

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": "ProofOfMarks",
  "version": "1.0.0",
  "name": "ProofOfMarks",
  "author": "did:example:issuer",
  "authored": "2024-01-01T00:00:00Z",
  "schema": {
    "$id": "proof-of-marks.json",
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "properties": {
      "studentName": { "type": "string" },
      "marks": { "type": "number" }
    },
    "required": ["studentName", "marks"],
    "additionalProperties": false
  }
}
```

### Wallet-interoperability config (`oid4vciConfig`)

A schema can opt into OpenID4VCI issuance by setting an `oid4vciConfig` block:

```json
{
  "oid4vciConfig": {
    "oid4vciEnabled": true,
    "oid4vciFormats": ["ldp_vc", "jwt_vc_json", "vc+sd-jwt", "mso_mdoc"],
    "display": [{ "name": "Proof of Marks", "locale": "en" }],
    "vct": "ProofOfMarks",
    "mdoc": { "docType": "org.iso.18013.5.1.mDL", "namespace": "org.iso.18013.5.1" },
    "renderMethod": { "type": "SvgRenderingTemplate2023", "name": "default", "svg": "..." }
  }
}
```

::: info
Only schemas with `oid4vciEnabled: true` are surfaced by the OID4VC service's credential-offer flow.
:::

## Credential Issuance API

```http
POST /credentials/issue
{
  "credential": { "...W3C credentialSubject fields..." },
  "credentialSchemaId": "proof-of-marks",
  "credentialSchemaVersion": "1.0.0",
  "tags": ["marks-2024"],
  "format": "ldp_vc"
}
```

The service:

1. Validates the subject against the schema
2. Mints the credential's id as a fresh DID (via the Identity service)
3. Optionally reserves a Status List index for future revocation
4. Signs the credential in the requested format — `ldp_vc` via jsonld-signatures Ed25519Signature2020/2018 or RsaSignature2018; `jwt_vc_json` / `vc+sd-jwt` / `mso_mdoc` via the Identity service's enveloped-proof signer

## Credential Verification API

```http
POST /credentials/verify
{
  "verifiableCredential": { "...signed VC..." },
  "options": { "challenge": "...", "domain": "..." }
}
```

```http
GET /credentials/{id}/verify
```

Response:

```json
{
  "status": "...",
  "checks": [{ "active": true, "revoke": false, "expired": false, "proof": true }],
  "warnings": [],
  "errors": []
}
```

Verification checks the signature proof and, if the credential carries a status-list entry, checks the corresponding bit for revocation.

## Revocation

```http
DELETE /credentials/{id}
```

Marks the credential `REVOKED` in the database and — when `STATUS_LIST_ENABLED` is set — flips its bit in a per-issuer Status List (bitstring, 100,000 entries per list, allocated on issuance). The signed Status List credential itself can be served:

```http
GET /credentials/status-list/{id}
GET /credentials/revocation-list?issuerId={issuerId}
```

## DID and key generation

```http
POST /did/generate
{
  "content": [
    { "method": "web", "keyPairType": "Ed25519VerificationKey2020" }
  ]
}
```

By default, DIDs are minted as `did:rcw:<uuid>`. Passing `method: "web"` produces `did:web:<host>:<uuid>` instead (host derived from `WEB_DID_BASE_URL`).

**Supported key types:** Ed25519VerificationKey2020/2018, RsaVerificationKey2018 and JsonWebKey2020 (EC P-256, used for `mso_mdoc`'s COSE ES256 signing).

::: tip
Keys are generated on request and held in Vault — never returned in plaintext.
:::

Resolution:

```http
GET /did/resolve/{id}
GET /{id}/did.json
```

## Wallet interoperability (OpenID4VCI / OpenID4VP)

Beyond the direct issue/verify APIs above, the OID4VC service exposes the same issuance and verification capability over open wallet protocols. This service now ships as part of the standard release build (`ghcr.io/sunbird-rc/sunbird-rc-oid4vc-service`), alongside Identity, Credential Schema and Credential Issuance.

:::: tabs
== Issuance (OpenID4VCI)

1. `POST /oid4vc/offer`
2. `GET /oid4vc/offer/:id`
3. `POST /oid4vc/token`
4. `POST /oid4vc/nonce`
5. `POST /oid4vc/credential` (or `/oid4vc/deferred` for async issuance)

Discovery via `/.well-known/openid-credential-issuer`.

== Verification (OpenID4VP)

1. `POST /vp/request` (DCQL)
2. `GET /vp/request-object/:id`
3. `POST /vp/response`
4. `GET /vp/status/:id`
::::

This lets any OpenID4VCI/VP-compliant wallet — not just a Sunbird-built one — fetch and present credentials issued through this service.

## Use cases

* Issuing and verifying academic transcripts and marksheets
* Employment verification (offer letters, experience certificates)
* Health credentials (vaccination, licenses)
* Government-issued certificates (birth, caste, income) with attestation workflows
* Cross-registry attested credentials (e.g. an education registry attesting a claim raised against a student registry)
