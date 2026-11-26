---
title: "Registry CLI"
---

# Registry CLI

::: info
**System requirements**: 4 cores · 8 GB RAM · 100 GB disk minimum.
:::

This guide assumes some familiarity with basic Linux commands. Don't copy-paste the `$` signs — they indicate that what follows is a terminal command.

:::: steps
::: step
### Install the Registry CLI

```bash
$ npm install --global @sunbird-rc/registry-cli
```

If you hit a permission-denied error, prefix the command with `sudo`:

```bash
$ sudo npm install --global @sunbird-rc/registry-cli
```

Check the install:

```bash
$ registry help
```
:::

::: step
### Set up a registry instance

Run the following in a directory where you wish to set up the registry (`~/Registries/example/` in this example):

```bash
$ mkdir -p ~/Registries/example
$ cd ~/Registries/example
$ registry init
```

This presents a set of questions to configure the registry — registry version, auxiliary services (toggle with SPACE BAR), and the QR code type to generate on certificates when signing is enabled. You can accept the defaults for a first run.
:::

::: step
### Check the registry status

```bash
$ registry status
```

Confirm every service shows as running. If a service shows `exited`, restart just that service:

```bash
$ docker-compose restart <service-name>
```

To force-recreate the registry service after a config or schema change:

```bash
$ SCHEMA_DIR=config/schemas docker-compose up -d --force-recreate --no-deps registry
```
:::

::: step
### Stop the registry

```bash
$ registry down
```
:::
::::

