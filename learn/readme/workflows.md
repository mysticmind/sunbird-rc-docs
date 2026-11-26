---
title: "Workflows"
description: "How users, issuers, holders and verifiers move through Sunbird RC — from onboarding to verification."
---

# Workflows

How users, issuers, holders and verifiers move through Sunbird RC — from onboarding to verification.

<figure><img src="/images/workflow-6b65f886.png" alt=""><figcaption></figcaption></figure>

The full flow runs from a trusted record to a verified credential. Each step is handled by one of Sunbird RC's two components:

| Step                        | Component                                                            |
| --------------------------- | -------------------------------------------------------------------- |
| Registration and onboarding | Registry                                                             |
| Credential issuance         | Credentials                                                          |
| Credential storage          | Holder's wallet (not part of Sunbird RC)                             |
| Credential verification     | Verifier, using Credentials APIs or any standards-compliant verifier |

You can start at either component. If you use the Registry, records flow from it into issuance. If you only use Credentials, issuance starts from your existing system of record instead.

:::: steps
::: step
### User registration and onboarding (Registry)

Users can join a registry in three ways:

* Self-registration
* Registration via invitation
* Integration with existing registries
:::

::: step
### Verifiable credential issuance (Credentials)

The issuer creates the credential from a trusted record — a Sunbird RC Registry entry or a record from another system — and digitally signs it using a cryptographic key that only the issuer can use (as JSON-LD, JWT, SD-JWT or mdoc, depending on the configured credential format).

The signature is generated with the issuer's private key and attached to the credential, so verifiers can confirm the credential hasn't been altered since it was issued. The public key associated with the issuer's private key can also be included in the credential, letting verifiers check the signature.
:::

::: step
### Verifiable credential storage (Holder)

Once issued, the credential is stored in an eLocker, digital wallet or other digital storage controlled by the credential holder. The wallet gives the holder a secure, convenient way to manage and share their credentials with others.
:::

::: step
### Verifiable credential verification (Verifier)

When the holder presents a credential to an accepting party or verifier — such as a potential employer — the verifier checks its authenticity using cryptographic techniques. Verifying the issuer's digital signature confirms that the credential hasn't been tampered with since it was issued, and checking its status confirms it hasn't been revoked.
:::
::::

## Wallet-based flows

The Credentials component also supports standards-based flows that work with **any compliant wallet**, not just a Sunbird-built one. These are provided by the optional OID4VC service.

:::: tabs
== Issuance (OpenID4VCI)

The issuer publishes a credential offer; the wallet resolves it, exchanges a pre-authorized code for an access token, and fetches the signed credential directly into wallet storage — a standardized, wallet-interoperable alternative to manual download.

== Verification (OpenID4VP)

The verifier describes the claims it needs using DCQL; the wallet returns a signed presentation containing only those claims, which the verifier checks against the issuer's public key.
::::

