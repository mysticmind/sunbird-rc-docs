---
title: "Create A Property Of An Entity"
description: "To add property to an existing entity, we need to make the following HTTP request"
---

# Create A Property Of An Entity

To add property to an existing entity, we need to make the following HTTP request

## Create a property in already existing entity

<mark style="color:var(--vp-c-green-1);">`POST`</mark> `/api/v1/{entity-type}/{id}/{entity-property}`

#### Path Parameters

| Name                                              | Type   | Description                                                  |
| ------------------------------------------------- | ------ | ------------------------------------------------------------ |
| entity-type<mark style="color:var(--vp-c-red-1);">\*</mark>     | String | Type of entity to update                                     |
| id<mark style="color:var(--vp-c-red-1);">\*</mark>              | String | id of the entity to update                                   |
| entity-property<mark style="color:var(--vp-c-red-1);">\*</mark> | String | entity Property which to be added in already existing entity |

#### Headers

| Name                                           | Type   | Description                                                                                 |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| authorization                                  | String | Set to `Bearer {access-token}` if roles in Schema is not anonymous. Else token can be empty |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                                                   |

#### Request Body

| Name                                  | Type   | Description            |
| ------------------------------------- | ------ | ---------------------- |
| ...<mark style="color:var(--vp-c-red-1);">\*</mark> | Object | Property to be updated |

:::: tabs
== 200: OK

```json
{
    "id": "sunbird-rc.registry.update",
    "ver": "1.0",
    "ets": 1669113170690,
    "params": {
        "resmsgid": "",
        "msgid": "85057df5-d4d6-4e7b-8bb1-a774f689e9c8",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK"
}
```
::::

## Usage

::: code-group
```shell [cURL]
curl --location \
	--request 'POST' \
	--header 'content-type: application/json' \
	--header 'authorization: bearer {access-token}' \
	--data-raw '{
		"city": "Ahmedabad"
	}' \
	'{registry-url}/api/v1/{entity-type}/{id}/{entity-property}'
```
```shell [HTTPie]
printf '{
		"city": "Ahmedabad"
	}' | http POST \
	'{registry-url}/api/v1/{entity-type}/{id}/{entity-property}' \
	'content-type: application/json' \
	'authorization: Bearer {access-token}'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
