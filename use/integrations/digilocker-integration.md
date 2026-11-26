---
title: "Digilocker Integration"
---

# Digilocker Integration

Covers pulling Sunbird RC-issued credentials into the DigiLocker wallet.

::: info
**Prerequisites**

* A [DigiLocker partner account](https://www.digilocker.gov.in/web/partners/)
* Familiarity with the [DigiLocker Issuer API spec](https://cf-media.api-setu.in/resources/DigiLocker-Issuer-APISpecification-v1-13.pdf)
:::

::: warning
DigiLocker has no sandbox — all testing happens against production. Be careful with changes in the partner portal.
:::

## Onboarding Sunbird RC in DigiLocker

:::: steps
::: step
### Add a Pull URI Request

Log in to the partner account → **Pull URI Request** section → **+ Add**.
:::

::: step
### Fill in the callback details

The VC pull URL, e.g. `https://<host>/digilocker/v1/digilocker/pullUriRequest`, and the HMAC key used to verify DigiLocker's request signatures. Then Next.
:::

::: step
### Define the user parameters

Which parameters get sent to your backend to fetch the VC — existing profile fields like Aadhaar, or custom parameters like a Certificate ID. Then Next.
:::

::: step
### Add the document type

Add the document type being fetched → Update.
:::

::: step
### Test and publish

Test via **Test Service** — a correct config returns the VC certificate. Then publish; only published configs are visible to users in the DigiLocker portal.
:::
::::

## Configure Sunbird RC to serve VCs to DigiLocker

Requires a JSON mapping file per document type:

```json
{
  "docType": {
    "schema": "Schema",
    "template": "html",
    "searchFilter": { "filters": { "osid": { "eq": "{{.certificate_id}}" } } }
  }
}
```

| Key            | Meaning                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------- |
| `docType`      | The document type configured in DigiLocker                                               |
| `schema`       | The schema the VC is fetched from                                                        |
| `template`     | The rendering template key                                                               |
| `searchFilter` | Search parameters (matching DigiLocker's Add New API step) used to locate the credential |

Sunbird RC fetches the credential as a PDF and returns an XML response to DigiLocker.

```json [Example — Pre-Matric Scholarship]
{
  "SACER": {
    "schema": "PreMatricScholarship",
    "template": "html",
    "searchFilter": { "filters": { "osid": { "eq": "{{.certificate_id}}" } } }
  }
}
```

