---
title: "Credentialling Services setup (Dev / Docker / Helm)"
---

# Credentialling Services setup (Dev / Docker / Helm)

The same three-way split as the Registry: run locally for development, bring it up with Docker Compose, or deploy to Kubernetes with Helm.

:::::: tabs
== Development

* Node.js version: `v20.11.0`
* Runs identity-service, credential-schema, and credentials-service locally. Vault is required — see Working with the Vault.
* Environment variables: check the [docker-compose.yml](https://github.com/Sunbird-RC/sunbird-rc-core/blob/main/docker-compose.yml) for the values credentialling services expect (e.g. `DATABASE_URL=postgres://postgres:postgres@db:5432/registry`).
* Per service: `cd` into the service directory, `yarn install`, then `yarn start`.

**Dependency chain**

```mermaid
flowchart LR
    Vault --> Identity[Identity Service]
    DB[(Database)] --> Identity
    DB --> Schema[Credential Schema Service]
    Identity --> Schema
    DB --> Creds[Credentials Service]
    Identity --> Creds
    Schema --> Creds
```

== Docker Compose

* System requirements: 4 Cores / 8 GB RAM / 100 GB disk (same as Registry).
* Download the [credentialling docker-compose.yml](https://github.com/Sunbird-RC/devops/blob/main/deploy-as-code/docker/v2/credentialling/docker-compose.yml) from the `devops` repo.
* Create a `.env` from the example file provided alongside it.

```bash
docker-compose up -d
docker-compose ps
```

Swagger: `<base-url>/docs`

== Helm

::: warning
Same trip-up as the Registry Helm page: this deploys from `Sunbird-RC/devops`, not a `deployment` repo, and the credentialling charts live specifically at `deploy-as-code/helm/v2/credentialling`.
:::

System requirements and prerequisites are the same as the Registry Helm setup, plus the [High-Level Architecture](/registry/technical-overview/high-level-architecture) page is worth a read first.

:::: steps
::: step
#### Clone the repo

```bash
git clone https://github.com/Sunbird-RC/devops.git
cd devops/deploy-as-code/helm/v2/credentialling
```

Pre-check and namespace creation: same commands as the Registry Helm flow.
:::

::: step
#### Deploy Vault

Credentialling Services use HashiCorp Vault as the keystore. Follow [HashiCorp's Kubernetes Raft deployment guide](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-raft-deployment-guide) in the same namespace you created above, then:

1. **Initialize** (first time only): `vault operator init` — save the unseal keys and root token securely. Base64-encode the root token as `VAULT_SECRET_TOKEN` in `values.yaml`.
2. **Unseal**: `vault operator unseal`, repeated with enough distinct unseal keys to reach the threshold (typically 3).
3. **Log in**: `vault login <root_token>`.
4. **Enable a KV engine**: `vault secrets enable -path=kv kv-v2` — whatever path you choose here must match `root_path: http://vault:8200/v1/kv` in `values.yaml`.
:::

::: step
#### Create secrets and deploy

In `values.yaml`, base64-encoded:

* `VAULT_SECRET_TOKEN` — the initial root token *(mandatory)*
* `DB_URL` — e.g. <code v-pre>postgres://{{username}}:{{password}}@localhost:5432/{{database_name:sunbirdrc}}</code> *(mandatory)*

```bash
helm upgrade --install --namespace=demo-registry demo-registry helm_charts --create-namespace
kubectl get pods -n demo-registry
```
:::
::::
::::::

## Service configuration

Environment variables passed to each credentialling service.

:::: tabs
== Identity Service

| Env var            | Description                                                                       |
| ------------------ | --------------------------------------------------------------------------------- |
| `DATABASE_URL`     | `postgres://<username>:<password>@<db_url>:<db_port>/<db_name>`                   |
| `VAULT_ADDR`       | Address for the HashiCorp Vault, e.g. `http://<vault_address>:8200/v1`            |
| `VAULT_TOKEN`      | Vault API token                                                                   |
| `VAULT_ROOT_PATH`  | Vault root path for the key-value store, e.g. `http://<vault_address>:8200/v1/kv` |
| `VAULT_TIMEOUT`    | API timeout for Vault in ms (e.g. `5000`)                                         |
| `VAULT_PROXY`      | `false`                                                                           |
| `JWKS_URI`         | JWKS URI of the OAuth2 resource server for handling Bearer tokens                 |
| `ENABLE_AUTH`      | Enable/disable authentication (e.g. `false`)                                      |
| `WEB_DID_BASE_URL` | Base URL to generate a web-based DID                                              |

Supported signature suites: `Ed25519Signature2020`, `Ed25519Signature2018`, `RSASignature2018`.

== Credential Schema Service

| Env var             | Description                                                     |
| ------------------- | --------------------------------------------------------------- |
| `DATABASE_URL`      | `postgres://<username>:<password>@<db_url>:<db_port>/<db_name>` |
| (identity endpoint) | `http://identity-service:3332`                                  |
| `JWKS_URI`          | JWKS URI of the OAuth2 resource server                          |
| `ENABLE_AUTH`       | Enable/disable authentication                                   |

== Credential Issuance Service

| Env var                       | Description                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| `DATABASE_URL`                | `postgres://<username>:<password>@<db_url>:<db_port>/<db_name>`                            |
| `CREDENTIAL_SERVICE_BASE_URL` | Base URL for the credential service, used to set the verify URL in the QR code             |
| `JWKS_URI`                    | JWKS URI of the OAuth2 resource server                                                     |
| `ENABLE_AUTH`                 | Enable/disable authentication                                                              |
| `QR_TYPE`                     | Set to `W3C_VC` to embed a compressed VC in the QR code instead of a verify-credential URL |
::::
