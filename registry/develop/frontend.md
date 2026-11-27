---
title: "Setup Frontend"
---

# Setup Frontend

Get the latest code from the Sunbird RC UI repository — an **Angular 10** project. Install dependencies and run.

<a href="https://github.com/Sunbird-RC/sunbird-rc-ui" class="button primary" data-icon="github">Sunbird RC/sunbird-rc-ui</a>

## Configuration

Example config lives in `src/examples`. Key pieces:

* API base URL / schema URL for your deployment
* `forms.json` in `src/assets/config` — defines form schemas per entity, built on [formly.dev](https://formly.dev/)

| `forms.json` key                      | Contains                               |
| ------------------------------------- | -------------------------------------- |
| `fields`                              | name, class, required, disabled        |
| `layout`                              | api, title                             |
| `blocks`                              | definition, title, add, edit, multiple |
| `fields.includes` / `fields.excludes` | Response field filtering               |

## Proxy configuration

To avoid CORS locally:

```bash
npm start
# or
ng serve --proxy-config proxy.conf.json
```

## Hosting the frontend

As a container (image built from the Angular build output), on a VM, or from blob storage (e.g. S3 behind a CDN).
