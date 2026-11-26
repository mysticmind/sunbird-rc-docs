---
title: "Wallet Integration"
---

# Wallet Integration

::: info
**Applies to** Sunbird RC v2.1.0 and later · **Service** `oid4vc-service` · **Protocols** OpenID4VCI 1.0, OpenID4VP 1.0/draft-23
:::

From v2.1.0, Sunbird RC speaks wallet protocols directly — a conformant wallet can receive a credential from a Sunbird RC issuer and present it back to a Sunbird RC verifier with zero Sunbird-specific integration (no SDK, no issuer pre-registration, no proprietary API).

:::: steps
::: step
### Demo apps

Two thin reference UIs over the public `oid4vc-service` endpoints demonstrate both halves of the flow (issuer and verifier), with no privileged access beyond what a third party could build.
:::

::: step
### Issuer flow

A schema must opt in with an `oid4vciConfig` block (`oid4vciEnabled: true`, plus `oid4vciFormats`) before it's visible to wallets. Discovery is a live lookup, so newly-opted-in schemas show up immediately — no cache to bust.
:::

::: step
### Verifier flow

Pick or write a DCQL query in the verifier app → scan the presentation-request QR with the same wallet → consent to disclosure.

The verifier's status panel reports six checks: `holderSignature`, `nonce`, `credentialSignatures`, `holderBinding`, `revocation`, `dcql`. All six passing means the presenter controls the holder key, the credential is genuine and unrevoked, it's bound to that holder, and the disclosed claims satisfy the query exactly. Any failure shows which stage failed.
:::
::::

For the curl-level setup and full API walkthrough, see `services/oid4vc-service/README.md` §5 (deployment) and §6 (manual testing) in the `sunbird-rc-core` repo.

## Wallet compatibility flags

Three flags exist purely to accommodate wallets at different points on the OpenID4VC standards timeline. None affect the credential itself, only the protocol envelope.

| Flag                             | Default | Effect                                                                                                                                                                                                                                            |
| -------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DRAFT13_COMPAT_MODE`            | `false` | Emit OpenID4VCI draft-13 shapes instead of final 1.0 (`credentials_supported` in metadata, `credentials` in the offer object, `user_pin_required` in the grant, retained `c_nonce` in the token response). Needed by the MOSIP Inji Wallet today. |
| `OID4VP_SIGN_REQUEST`            | `true`  | Sign the OpenID4VP request object as a JAR with a `did:`-prefixed `client_id`. Set `false` for unsigned plain JSON; overridable per-request via `{"signed": false}`.                                                                              |
| `OID4VP_LEGACY_CLIENT_ID_SCHEME` | `false` | Emit the pre-draft-22 shape — `client_id` is the bare `response_uri`, with `client_id_scheme: "redirect_uri"` as a separate field, unsigned. Needed by walt.id.                                                                                   |

**OpenID4VP request modes**

| Mode               | `client_id`                                    | Signing                                | Selected by                           |
| ------------------ | ---------------------------------------------- | -------------------------------------- | ------------------------------------- |
| signed *(default)* | `did:<VERIFIER_DID>`                           | JWS, `application/oauth-authz-req+jwt` | `OID4VP_SIGN_REQUEST` unset or `true` |
| unsigned           | `<response_uri>`                               | none, plain JSON                       | `{"signed": false}` per request       |
| legacy             | `<response_uri>` + separate `client_id_scheme` | none, plain JSON                       | `OID4VP_LEGACY_CLIENT_ID_SCHEME=true` |

::: info
Per spec, the `redirect_uri` client-id scheme must never be signed — which is why choosing signed mode forces the `did:` prefix.
:::

## What the wallet actually talks to

Issuer/verifier-side calls like `POST /oid4vc/offer` and `POST /vp/request` are never wallet-facing.

:::: tabs
== Issuance (OpenID4VCI)

| Endpoint                                    | Purpose                                                     |
| ------------------------------------------- | ----------------------------------------------------------- |
| `GET /.well-known/openid-credential-issuer` | Discovery, live from `credential-schema`'s opted-in schemas |
| `GET /oid4vc/offer/:id`                     | Dereference the offer deep link                             |
| `POST /oid4vc/token`                        | `pre-authorized_code` grant → access token + `c_nonce`      |
| `POST /oid4vc/credential`                   | Proof-of-possession JWT → signed credential                 |
|
                                |                                                             |

== Presentation (OpenID4VP)

| Endpoint                            | Purpose                                      |
| ----------------------------------- | -------------------------------------------- |
| `GET /vp/request-object/:id`        | Fetch the request object (JWS or plain JSON) |
| `POST /vp/response` (`direct_post`) | Submit the `vp_token`                        |
|
                        |                                              |
|
::::
                       |                                              |

Deep links: `openid-credential-offer://...` (offers), `openid4vp://...` (presentation requests) — both delivered as `qr_data`. Holder binding accepts either a resolvable DID (`kid` in the PoP JWT) or an inline JWK/`did:jwk`, so wallets that don't publish DIDs still work. `oid4vc-service` itself holds no credential keys or storage — only short-lived session state and its own protocol signing key (which lives in Vault via `identity-service`).

For the complete env-var reference (TTL settings, Keycloak auth setup, per-schema issuer DID behavior), see `services/oid4vc-service/README.md` §4 in the `sunbird-rc-core` repo.

::: tip
**Verified wallet interop** — beyond the self-driven test harness (all four credential formats issue and verify end-to-end), `jwt_vc_json` and `vc+sd-jwt` issuance and presentation have been confirmed against independent third-party wallet implementations.
:::

