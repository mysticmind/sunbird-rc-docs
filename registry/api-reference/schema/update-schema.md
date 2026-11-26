---
title: "Update Schema"
---

# Update Schema

## Request

## Create a Schema

<mark style="color:var(--vp-c-brand-1);">`PUT`</mark> `/api/v1/Schema/{id}`

#### Path Parameters

| Name                                 | Type   | Description                            |
| ------------------------------------ | ------ | -------------------------------------- |
| id<mark style="color:var(--vp-c-red-1);">\*</mark> | String | id of the schema that is to be updated |

#### Headers

| Name                                           | Type   | Description                                                        |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------ |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                          |
| authorization                                  | String | Set to `Bearer {access-token}` . The token should be a admin token |

#### Request Body

| Name                                  | Type | Description       |
| ------------------------------------- | ---- | ----------------- |
| ...<mark style="color:var(--vp-c-red-1);">\*</mark> |      | The entity's data |

:::: tabs
== 200: OK Success Response of Updated Schema

```javascript
{
    "id": "sunbird-rc.registry.update",
    "ver": "1.0",
    "ets": 1669117705369,
    "params": {
        "resmsgid": "",
        "msgid": "2ff44354-bb9a-4dce-93ba-053f97587df6",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK"
}
```
::::

Sample Schema Request Payload

```json
{
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}
```

### Usage

::: code-group
```shell [cURL]
curl --location --request PUT '{registry-url}/api/v1/Schema/{id}' \
--header 'Authorization: Bearer {access-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}'
```
```shell [HTTPie]
printf '{
  "schema": "{   \"$schema\": \"http://json-schema.org/draft-07/schema\",   \"type\": \"object\",   \"properties\": {      \"Place\": {         \"$ref\": \"#/definitions/Place\"      }   },   \"required\": [      \"Place\"   ],   \"title\": \"Place\",   \"definitions\": {      \"Place\": {         \"$id\": \"#/properties/Place\",         \"type\": \"object\",         \"title\": \"The Place Schema\",         \"required\": [            \"name\",            \"city\"],         \"properties\": {            \"name\": {               \"type\": \"string\"            },            \"city\": {               \"type\": \"string\"            }},   \"_osConfig\": {      \"privateFields\": [         \"name\"      ],      \"signedFields\": [],      \"roles\": [         \"anonymous\"      ],      \"ownershipAttributes\": [],      \"attestationPolicies\": [         {            \"name\": \"schemaAttestation\",            \"conditions\": \"(ATTESTOR#$.[*]#.contains('board-cbse'))\",            \"type\": \"MANUAL\",            \"attestorPlugin\": \"did:internal:ClaimPluginActor?entity=board-cbse\",            \"attestationProperties\": {}         }      ],      \"credentialTemplate\": {         \"@context\": [            \"https://www.w3.org/2018/credentials/v1\",            \"{someUrlForTemplate}\"         ],         \"type\": [            \"VerifiableCredential\",            \"{TypeOfCertificate}\"         ],         \"issuer\": \"{issuerName}\",         \"issuanceDate\": \"{issuanceDate}\",         \"credentialSubject\": {            \"type\": \"Place\",            \"name\": \"{name}\"},         \"evidence\": {            \"type\": \"{SomeType}\"}},      \"certificateTemplates\": {        \"html\": \"{templateUrl}\"      }   }}}}"
}'| http  PUT '{registry-url}/api/v1/Schema' \
 Authorization:'Bearer {access-token}' \
 Content-Type:'application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
