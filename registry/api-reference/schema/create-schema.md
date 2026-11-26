---
title: "Create Schema"
---

# Create Schema

## Request

## Create a Schema

<mark style="color:var(--vp-c-green-1);">`POST`</mark> `/api/v1/Schema`

#### Headers

| Name                                           | Type   | Description                                                        |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------ |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                          |
| authorization                                  | String | Set to `Bearer {access-token}` . The token should be a admin token |

#### Request Body

| Name                                     | Type   | Description        |
| ---------------------------------------- | ------ | ------------------ |
| name<mark style="color:var(--vp-c-red-1);">\*</mark>   | string | schema name        |
| schema<mark style="color:var(--vp-c-red-1);">\*</mark> | string | json schema        |
| status                                   | String | DRAFT \| PUBLISHED |

:::: tabs
== 200: OK Success Response of entity Created

```javascript
{
    "id": "sunbird-rc.registry.create",
    "ver": "1.0",
    "ets": 1669113026569,
    "params": {
        "resmsgid": "",
        "msgid": "7b15f6ee-eb5b-4a13-ba79-f70b3ab54fc3",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK",
    "result": {
        "Schema": {
            "osid": "1-1a2f15e7-6c54-40e9-a689-68628a3d69df"
        }
    }
}
```
::::

Sample Schema Request Payload

```json
{
  "name": "{schema-name}",
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}
```

Important Fields in Response Body

| Field                  | Type     | Description                                                                                     |
| ---------------------- | -------- | ----------------------------------------------------------------------------------------------- |
| `result.{Schema}.osid` | `string` | The ID of the created schema in the registry, used for retrieval and modification of the entity |

### Usage

::: code-group
```shell [cURL]
curl --location --request POST '{registry-url}/api/v1/Schema' \
--header 'Authorization: Bearer {access-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "{schema-name}",
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}'
```
```shell [HTTPie]
printf '{
  "name": "{schema-name}",
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}'| http  POST '{registry-url}/api/v1/Schema' \
 Authorization:'Bearer {access-token}' \
 Content-Type:'application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
