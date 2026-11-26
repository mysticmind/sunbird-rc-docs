---
title: "Get An Entity By Id"
description: "To get an entity, we need to make the following HTTP request"
---

# Get An Entity By Id

To get an entity, we need to make the following HTTP request

<mark style="color:blue;">`GET`</mark> `/api/v1/{entity-type}/id`

#### Path Parameters

| Name                                          | Type   | Description                      |
| --------------------------------------------- | ------ | -------------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | The type of entity to retrieve   |
| id<mark style="color:red;">\*</mark>          | String | The ID of the entity to retrieve |

#### Headers

| Name                                            | Type   | Description                                                                                                                                                                  |
| ----------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| authorization<mark style="color:red;">\*</mark> | String | Set to `Bearer {access-token}` if roles in schema is not anonymous. Else authorization can be empty                                                                          |
| content-type<mark style="color:red;">\*</mark>  | String | Set to `application/json` to retrieve in json. Other allowed values include `application/vc+ld+json`, `application/ld+json`, `application/pdf`, `image/svg+xml`, `text/html` |
| template-key                                    | String | `template-key` is an optional header, it can be used for `pdf/html/svg` content type. It should be one of the keys mentioned in certificateTemplates in the schema config.   |
| template                                        | String | `template` is an optional header where we can pass the URL of the external template directly in the API. To use this `enable_external_templates` ENV needs to be enabled     |
| viewTemplateId                                  | String | File name of view templates configured                                                                                                                                       |

:::: tabs
== 200: OK Response when content-type is application/json

```javascript
{
	"phoneNumber": "1234567890",
	"school": "UP Public School",
	"subject": "Math",
	"name": "Pranav Agate",
	"osid": "{id}",
	"osOwner": ["{owner-id}"],
	"_osState/school": "DRAFT"
}
```
::::

Important variables in the response body:

| Field              | Type   | Description                                                                                                                                                                                                                            |
| ------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_osState/{field}` | String | State of an attestable field. Can be `DRAFT` (when it has not been sent for attestation), `ATTESTATION_REQUESTED` (when sent for attestation), `PUBLISHED` (when successfully attested) and `REJECTED` (when rejected by the attestor) |
| \_osOwner          | String | User ID of the entity in Keycloak.                                                                                                                                                                                                     |
