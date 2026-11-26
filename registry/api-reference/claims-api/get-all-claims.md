---
title: "Get All Claims"
---

# Get All Claims

<mark style="color:blue;">`GET`</mark> `/api/v1/{entity-name}/claims`

#### Path Parameters

| Name                                          | Type   | Description                                              |
| --------------------------------------------- | ------ | -------------------------------------------------------- |
| entity-name<mark style="color:red;">\*</mark> | String | Name of the entity to which attestation request was sent |

#### Query Parameters

| Name | Type   | Description                                      |
| ---- | ------ | ------------------------------------------------ |
| page | String | Page no if you want response in pagenated format |
| size | String | Maximum claims claims to be returned in one page |

#### Headers

| Name                                           | Type   | Description                                                                                        |
| ---------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                          |
| authorization                                  | String | Set to `Bearer {access-token}` if `roles` in schema config is not anonymous else this can be empty |

:::: tabs
== 200: OK

```javascript
{
    "totalPages": "",
    "content": [
        {
            "id": "{claimId}",
            "entity": "{entityName",
            "entityId": "{entityId}",
            "status": "OPEN",
            "attestationId": "{attestationID}",
            "attestationName": "{attestationName}",
            "closed": false
            ...
        }
    ]
    "totalElements": ""
}
```
::::

### Usage

#### cURL

```shell
curl --location --request GET '{registry-url}/api/v1/{entity-name}/claims?page=1&size=10' \
--header 'Authorization: Bearer {access-token}'
```

#### HTTPie

```shell
http GET '{registry-url}/api/v1/{entity-name}/claims?page=1&size=10' \
 Authorization:'Bearer {access-token}' \
```

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
