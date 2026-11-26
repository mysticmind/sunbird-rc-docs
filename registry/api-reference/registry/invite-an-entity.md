---
title: "Invite An Entity"
description: "To invite an entity, we need to make the following HTTP request"
---

# Invite An Entity

To invite an entity, we need to make the following HTTP request

## Invite an Entity

<mark style="color:green;">`POST`</mark> `/api/v1/{entity-type}/invite`

#### Path Parameters

| Name                                          | Type   | Description                  |
| --------------------------------------------- | ------ | ---------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | The type of entity to create |

#### Headers

| Name                                           | Type   | Description                                                                                              |
| ---------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                                |
| authorization                                  | String | Set to `Bearer {access-token}` if `inviteRoles` in schema config is not anonymous else this can be empty |

#### Request Body

| Name                                  | Type   | Description       |
| ------------------------------------- | ------ | ----------------- |
| ...<mark style="color:red;">\*</mark> | Object | The entity's data |

:::: tabs
== 200: OK Success response of entity invited

```json
{
	"id": "sunbird-rc.registry.invite",
	"ver": "1.0",
	"ets": 1634198998956,
	"params": {
		"resmsgid": "",
		"msgid": "3ee6a76f-d6c8-4262-a7ee-ddbe66fcb127",
		"err": "",
		"status": "SUCCESSFUL",
		"errmsg": ""
	},
	"responseCode": "OK",
	"result": { "Teacher": { "osid": "1-9d6099fc-2c01-4714-bceb-55ff28c482f9" } }
}
```
::::

Important Fields in Response Body

| Field                       | Type     | Description                                                                                    |
| --------------------------- | -------- | ---------------------------------------------------------------------------------------------- |
| `result.{entity-type}.osid` | `string` | The ID of the create entity in the registry, used for retrieval and modification of the entity |

## Usage

So to create a `Teacher` entity named Pranav Agate who teaches Math at UP Public School, we would make the following API call:

::: code-group
```shell [cURL]
curl --location \
	--request 'POST' \
	--header 'content-type: application/json' \
	--data-raw '{
		"phoneNumber": "1234567890",
		"school": "UP Public School",
		"subject": "Math",
		"name": "Pranav Agate",
	}' \
	'{registry-url}/api/v1/Teacher/invite'
```
```shell [HTTPie]
printf '{
    "name": "Pranav Agate",
    "teaches": "Math",
    "school": "UP Public School"
}'| http POST '{registry-url}/api/v1/Teacher/invite' \
 Content-Type:'application/json'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.

#### Note: Invite API doesn't validate the required parameters. Invite API is designed to be used to invite another actor to the system with minimal information, hence required validations will not be applied. Instead, use [create an entity API](/registry/api-reference/registry/create-an-entity).
