---
title: "Create An Entity"
description: "To create an entity, we need to make the following HTTP request"
---

# Create An Entity

To create an entity, we need to make the following HTTP request

## Request

## Create a record for entity-type

<mark style="color:green;">`POST`</mark> `/api/v1/{entity-type}`

#### Path Parameters

| Name                                          | Type   | Description                  |
| --------------------------------------------- | ------ | ---------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | The type of entity to create |

#### Query Parameters

| Name        | Type   | Description                                                                                                                                                          |
| ----------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mode        | String | Query parameter whose value can be `async` if creating an entity should be asynchronously handled                                                                    |
| callbackUrl | String | Query parameter whose value will be a `web-hook url`. The webook will be called once the entity is created in the registry. This is applicable only for `async mode` |

#### Headers

| Name                                           | Type   | Description                                                                                        |
| ---------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                          |
| authorization                                  | String | Set to `Bearer {access-token}` if `roles` in schema config is not anonymous else this can be empty |

#### Request Body

| Name                                  | Type | Description       |
| ------------------------------------- | ---- | ----------------- |
| ...<mark style="color:red;">\*</mark> |      | The entity's data |

:::: tabs
== 200: OK Success Response of entity Created

```javascript
{
	"id": "sunbird-rc.registry.create",
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
	"result": { "{entityName}": { "osid": "1-9d6099fc-2c01-4714-bceb-55ff28c482f9" } }
}
```
::::

Sample Request Body for Teacher as Entity-Type

```json
{
 "name": "Sunbird",
 "school": "UP Public School",
 "phoneNumber": "1234567890",
 "subject": "Math"
}
```

Important Fields in Response Body

<table><thead><tr><th width="261.3333333333333">Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>result.{entity-type}.osid</code></td><td><code>string</code></td><td>The ID of the create entity in the registry, used for retrieval and modification of the entity</td></tr></tbody></table>

### Usage

So to create a `Teacher` entity named Pranav Agate who teaches Math at UP Public School, we would make the following API call:

::: code-group
```shell [cURL]
curl --location \
	--request 'POST' \
	--header 'content-type: application/json' \
	--data-raw '{
		{
            "name": "Pranav Agate",
            "school": "UP Public School",
            "subject": "Math",
            "contact": "1234567890"
        }
	}' \
	'{registry-url}/api/v1/{entity-type}/'
```
```shell [HTTPie]
printf '{
            "name": "Pranav Agate",
            "school": "UP Public School",
            "subject": "Math",
            "contact": "1234567890"
        }' | http post \
	'{registry-url}/api/v1/{entity-type}' \
	'content-type: application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
