---
title: "Swagger JSON API"
---

# Swagger JSON API

## Returns all available registry apis

<mark style="color:var(--vp-c-indigo-1);">`GET`</mark> `/api/docs/swagger.json`

:::: tabs
== 200: OK Success Response

```json
{
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ],
    "schemes": [
        "https"
    ],
    "swagger": "2.0",
    "info": {
        "description": "Sunbird registry and credential api (SunbirdRC)",
        "title": "Sunbird Registry and Credential",
        "version": "1.0.0"
    },
    "host": "ndear.xiv.in",
    "basePath": "/",
    "paths": {
        ...
    },
    "definitions": {
        ...
    }
}
```
::::

