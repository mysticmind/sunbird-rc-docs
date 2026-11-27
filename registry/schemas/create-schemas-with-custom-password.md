---
title: "Create Schemas With Custom Password"
---

# Create Schemas With Custom Password

Configure a schema so entities can set their own password, using a Student example.

::::: steps
:::: step
### Configure the schema

Via the [Schema API Endpoint](/registry/api-reference/schema/create-schema):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "definitions": {
    "Student": {
      "required": ["name", "phoneNumber", "email", "school"],
      "uniqueIndexFields": ["phoneNumber"],
      "properties": {
        "name": { "type": "string" },
        "phoneNumber": { "type": "string" },
        "email": { "type": "string" },
        "school": { "type": "string" },
        "password": { "type": "string", "minLength": 8 }
      }
    }
  },
  "_osConfig": {
    "ownershipAttributes": [
      { "email": "/email", "mobile": "/phoneNumber", "userId": "/phoneNumber", "password": "/password" }
    ],
    "inviteRoles": ["anonymous"]
  }
}
```

::: warning
If `password` isn't set as an ownership attribute, Sunbird RC falls back to the default password configured in the registry environment. Passwords only apply at creation — they can't be changed via the update-entity API, and if the user account already exists (created by another entity), the password won't be updated.
:::
::::

::: step
### Invite the entity

Via the [Invite Entity API Endpoint](/registry/api-reference/registry/invite-an-entity):

```bash
curl --location --request POST \
  --header 'content-type: application/json' \
  --data-raw '{ "name": "Pranav Agate", "phoneNumber": "1234567890", "email": "pranav@upps.in", "school": "UP Public School", "password": "pranav@1234" }' \
  'http://localhost:8081/api/v1/Student/invite'
```

This creates the entity and a matching IAM (Keycloak) user with that password.
:::

::: step
### Get an access token

```bash
curl --location --request POST \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data 'client_id=registry-frontend' --data 'username=1234567890' --data 'password=pranav@1234' --data 'grant_type=password' \
  'http://localhost:8080/auth/realms/sunbird-rc/protocol/openid-connect/token'
```
:::

::: step
### Retrieve the entity

Via the [Retrieve Entity API Endpoint](/registry/api-reference/registry/get-an-entity):

```bash
curl --location --request GET \
  --header 'content-type: application/json' \
  --header 'authorization: bearer {access-token}' \
  'http://localhost:8081/api/v1/Student'
```

The password is never returned — it's only used at Keycloak account creation and isn't stored in the entity record.
:::
:::::

