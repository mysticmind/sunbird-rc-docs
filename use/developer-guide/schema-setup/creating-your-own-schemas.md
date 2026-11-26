---
title: "Creating Your Own Schemas"
---

# Creating Your Own Schemas

An entity is defined by its schema.

```json [student.json]
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "type": "object",
  "definitions": {
    "Student": {
      "$id": "#/properties/Student",
      "type": "object",
      "uniqueIndexFields": ["phoneNumber"],
      "properties": {
        "name": { "type": "string" },
        "phoneNumber": { "type": "string" },
        "email": { "type": "string" },
        "school": { "type": "string" },
        "passwordToken": { "type": "string" }
      },
      "required": ["name", "phoneNumber", "email", "school"]
    }
  },
  "properties": { "Student": { "$ref": "#/definitions/Student" } },
  "_osConfig": {
    "privateFields": ["$.phoneNumber"],
    "internalFields": ["$.school"],
    "systemFields": ["osCreatedAt", "osUpdatedAt", "osCreatedBy", "osUpdatedBy"],
    "roles": ["admin"],
    "inviteRoles": ["admin"],
    "ownershipAttributes": [
      { "email": "/email", "mobile": "/phoneNumber", "userId": "/phoneNumber", "password": "/passwordToken" }
    ],
    "attestationPolicies": [
      {
        "name": "studentInstituteAttest",
        "additionalInput": { "enrollmentNumber": { "type": "string" } },
        "attestationProperties": { "name": "$.name", "educationDetails": "$.school" },
        "type": "MANUAL",
        "attestorPlugin": "did:internal:ClaimPluginActor?entity=Teacher",
        "conditions": "(ATTESTOR#$.school#.contains(REQUESTER#$.school#))"
      }
    ],
    "credentialTemplate": "",
    "certificateTemplates": {
      "svg": "https://raw.githubusercontent.com/dileepbapat/ref-sunbirdrc-certificate/main/schemas/templates/TrainingCertificate.svg"
    }
  }
}
```

::: info
The example above is annotated for clarity in prose — schema files themselves cannot contain comments.
:::

## Adding a new entity

Place the schema JSON in the schemas folder:

| Setup               | Schema folder                                                |
| ------------------- | ------------------------------------------------------------ |
| Registry CLI        | `config/schemas`                                             |
| Running from source | `java/registry/src/main/resources/public/_schemas`           |
| Docker Compose      | Wherever your `docker-compose.yaml` mounts the schema volume |

Then restart:

:::: tabs
== Docker Compose

```bash
$ docker compose up --force-recreate -d
```

== Registry CLI

```bash
$ registry restart
```
::::

::: info
`--force-recreate` is only needed after a config/schema change; for a plain process restart, `docker compose restart` or `registry restart --soft` is enough. After restarting manually, wait \~40 seconds and check status with `docker compose ps` / `registry status`.
:::

