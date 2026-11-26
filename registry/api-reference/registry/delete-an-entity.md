---
title: "Delete An Entity"
description: "To soft delete an entity, we need to make the following HTTP request"
---

# Delete An Entity

To soft delete an entity, we need to make the following HTTP request

## Deleting an Entity

<mark style="color:red;">`DELETE`</mark> `/api/v1/{entity-type}/{id}`

#### Path Parameters

| Name                                          | Type   | Description                  |
| --------------------------------------------- | ------ | ---------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | The type of entity to modify |
| entity-id<mark style="color:red;">\*</mark>   | String | The ID of entity to modify   |

#### Headers

| Name                                           | Type   | Description                                                                               |
| ---------------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                 |
| authorization                                  | String | Set to Bearer {access-token} if roles in Schema is not anonymous. Else token can be empty |

:::: tabs
== 200: OK Entity Deleted Success Response

```javascript
```
::::

## Usage

**cURL**

```
curl --location \
	 --request 'DELETE' \
	 --header 'content-type: application/json' \
	 --header 'authorization: Bearer {access-token}' \
	 '{registry-url}/api/v1/Teacher/{id}'
```

**HTTPie**

```
http DELETE \
	'{registry_url}/api/v1/Teacher/{id}' \
	'content-type: application/json' \
	'authorization: Bearer {access-token}'
```

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
