---
title: "Update An Entity"
description: "To update an entity, we need to make the following HTTP request"
---

# Update An Entity

To update an entity, we need to make the following HTTP request

## Updating an Entity

<mark style="color:orange;">`PUT`</mark> `/api/v1/{entity-type}/{id}`

#### Path Parameters

| Name                                          | Type   | Description                  |
| --------------------------------------------- | ------ | ---------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | The type of entity to modify |
| id<mark style="color:red;">\*</mark>          | String | The ID of entity to modify   |

#### Headers

| Name                                           | Type   | Description                                                                               |
| ---------------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| authorization                                  | String | Set to Bearer {access-token} if roles in schema is not anonymous. Else token can be empty |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                 |

#### Request Body

| Name                                  | Type   | Description       |
| ------------------------------------- | ------ | ----------------- |
| ...<mark style="color:red;">\*</mark> | String | The entity's data |

:::: tabs
== 200: OK Updated Entity Success Response

```javascript
{
	"id": "sunbird-rc.registry.update",
	"ver": "1.0",
	"ets": 1634371946769,
	"params": {
		"resmsgid": "",
		"msgid": "d51e6e6a-027d-4a42-84bb-2ce00e31d993",
		"err": "",
		"status": "SUCCESSFUL",
		"errmsg": ""
	},
	"responseCode": "OK"
}
```
::::

## Usage

### cURL

```
curl --location \
	--request 'PUT' \
	--header 'content-type: application/json' \
	--header 'authorization: bearer {access-token}' \
	--data-raw '{
		"phoneNumber": "1234567891",
		"school": "UP Public School",
		"subject": "Math",
		"name": "Pranav Agate",
	}' \
	'{registry-url}/api/v1/{entity-type}/{id}'
```

### HTTPie

```
printf '{
	"phoneNumber": "1234567891",
	"school": "UP Public School",
	"subject": "Math",
	"name": "Pranav Agate",
}' | http put \
	'{registry-url}/api/v1/{entity-type}/{id}' \
	'content-type: application/json' \
	'authorization: bearer {access-token}'
```

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
