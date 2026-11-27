---
title: "Helm Setup"
---

# Helm Setup

::: warning
**Helm charts don't live in `sunbird-rc-core` anymore.** They live in the separate [`Sunbird-RC/devops`](https://github.com/Sunbird-RC/devops) repo, under `deploy-as-code/helm/v1`. This is the single most common trip-up when following this page — an older doc revision pointed at `sunbird-rc-core/infra/...`, which no longer exists.
:::

**Prerequisites**: Kubernetes cluster (min. 3 nodes), Helm, kubectl, [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/), a Postgres DB (for both Keycloak and the registry), and optionally ElasticSearch, Kafka, Redis, Minio. See the [High-Level Architecture](/registry/architecture/high-level-architecture) page for what each optional service is for.

::::: steps
::: step
### Clone the repo and pre-check the cluster

```bash
git clone https://github.com/Sunbird-RC/devops.git
cd devops/deploy-as-code/helm/v1
```

```bash
kubectl cluster-info
kubectl get nodes
kubectl get ns
helm version
```

Create a namespace:

```bash
kubectl create ns demo-registry
```
:::

::: step
### Create secrets

Base64-encode all passwords/secrets and set them in `values.yaml`:

| Secret                           | Required | Purpose                                                     |
| -------------------------------- | -------- | ----------------------------------------------------------- |
| `DB_PASSWORD`                    | Yes      | Postgres database password                                  |
| `KEYCLOAK_ADMIN_PASSWORD`        | Yes      | Keycloak admin console password                             |
| `KEYCLOAK_DEFAULT_USER_PASSWORD` | Yes      | Default password for new users created by the registry      |
| `MINIO_SECRET_KEY`               | No       | Minio secret key                                            |
| `ELASTIC_SEARCH_PASSWORD`        | No       | ElasticSearch connection password                           |
| `KEYCLOAK_ADMIN_CLIENT_SECRET`   | No       | Client secret of the Keycloak admin client for the registry |
:::

:::: step
::: info
The passwords listed in the `values.yaml` should be updated.
:::
::::

::: step
### Configure values, schemas and signing keys

Modify the configuration values — database address, ElasticSearch address, etc. — in `values.yaml`.

Place schema files at [`devops/deploy-as-code/helm/v1/helm_charts/charts/registry/schemas`](https://github.com/Sunbird-RC/devops/tree/main/deploy-as-code/helm/v1/helm_charts/charts/registry/schemas).

Configure signing keys (a sample key ships by default — replace it before going live):

* Public + private signing keys: [`.../certificate-signer/keys`](https://github.com/Sunbird-RC/devops/tree/main/deploy-as-code/helm/v1/helm_charts/charts/certificate-signer/keys)
* Public key only (for verifiers): [`.../public-key-service/keys`](https://github.com/Sunbird-RC/devops/tree/main/deploy-as-code/helm/v1/helm_charts/charts/public-key-service/keys)
:::

::: step
### Deploy

```bash
helm upgrade --install --namespace=demo-registry demo-registry helm_charts --create-namespace
kubectl get pods -n demo-registry
```
:::

::: step
### Import the Keycloak realm and set the secret

Via the admin console (`<host>/auth/`): Master → Add realm → import `imports/realm-export.json`.

Then Clients → `admin-api` → Credentials → Regenerate Secret → copy it, base64-encode it, and set `KEYCLOAK_ADMIN_CLIENT_SECRET` via `kubectl edit secret rc-secret -n demo-registry`. Then:

```bash
kubectl rollout restart deploy/demo-registry -n demo-registry
kubectl get pods -n demo-registry
```
:::

::: step
### Check the registry APIs

Open `<host>/registry/api/docs/swagger.json` in a browser.
:::
:::::

