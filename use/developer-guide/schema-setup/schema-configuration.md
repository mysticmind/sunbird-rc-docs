---
title: "Schema Configuration"
---

# Schema Configuration

Sunbird RC uses standard JSON-LD schemas. Example — a `Place` concept with `name`, `city`, `addressRegion`, `country`:

```json [place.json]
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "type": "object",
  "properties": { "Place": { "$ref": "#/definitions/Place" } },
  "required": ["Place"],
  "title": "Place",
  "definitions": {
    "Place": {
      "$id": "#/properties/Place",
      "type": "object",
      "required": ["name", "city", "addressRegion", "country"],
      "properties": {
        "name": { "type": "string" },
        "city": { "type": "string" },
        "addressLocality": { "type": "string" },
        "addressRegion": { "type": "string" },
        "country": { "type": "string" },
        "postalCode": { "type": "string" },
        "contact": { "type": "string" },
        "email": { "type": "string" }
      }
    }
  }
}
```

## `_osConfig` extensions

Access, indexing, and primary-key behavior beyond plain JSON-LD.

| Key                                          | What it does                                                                                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `privateFields`                              | Visible to the owner and consenting third parties                                                                               |
| `internalFields`                             | Never exposed to any actor                                                                                                      |
| `systemFields`                               | `osCreatedAt`, `osUpdatedAt`, `osCreatedBy`, `osUpdatedBy`, `_osClaimId`, `_osCredentialId`, `_osSignedData`, `_osAttestedData` |
| `indexFields`                                | Index field set for faster lookups                                                                                              |
| `uniqueIndexFields`                          | Primary keys — enforces uniqueness                                                                                              |
| `roles` / `inviteRoles`                      | Gate CRUD and invite operations by Keycloak role; either can be `"anonymous"` for open access                                   |
| `ownershipAttributes`                        | Email/mobile/userId/password JSON paths, with `enableLogin: true`                                                               |
| `attestationPolicies`                        | List of attestation policies (see below)                                                                                        |
| `credentialTemplate`                         | W3C-compliant VC template, inline object or external URL                                                                        |
| `certificateTemplates.svg`                   | The visual-certificate template                                                                                                 |
| `PrivateFieldConfig` / `InternalFieldConfig` | How private/internal fields get emitted                                                                                         |
| `uniqueIdentifierFields`                     | Auto-generated formatted IDs (see below)                                                                                        |

Property types are String, Enum, Number, Integer, Object, Array, Boolean — see [type-specific keywords](https://json-schema.org/understanding-json-schema/reference/type).

Notification templates are configured per-schema, per-operation (`create`/`invite`/`update`/`delete`/`revoke`).
