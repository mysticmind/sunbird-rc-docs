---
title: "Pre-requisites"
---

# Pre-requisites

Install these before starting. What you need depends on the [path you choose](/use/getting-started). Each section has a command to confirm the install worked.

| Tool              | Version    | Needed for                                                    | Check with               |
| ----------------- | ---------- | ------------------------------------------------------------- | ------------------------ |
| Terminal emulator | —          | All paths                                                     | `echo Hi`                |
| Git               | any recent | All paths                                                     | `git --version`          |
| Docker            | any recent | All paths                                                     | `docker -v`              |
| Docker Compose    | 2.x        | All paths                                                     | `docker compose version` |
| Java              | 11         | Building the Registry from source                             | `java -version`          |
| NodeJS            | 20.x       | Registry CLI, or running the Credentials services from source | `node -v`                |

::: info
If you only run Sunbird RC with Docker Compose or Helm, you don't need Java or NodeJS.
:::

## Terminal emulator

Linux and macOS have a terminal installed already. For Windows, it's recommended you use `git-bash`, which you can install from [here](https://gitforwindows.org/).

Type `echo Hi` in the terminal once it's installed. If installed correctly, you should see `Hi` appear when you hit enter.

## Git

Installation instructions for Git can be found [here](https://git-scm.com/downloads).

```bash
$ git --version
```

## Docker

Installation instructions for Docker can be found [here](https://docs.docker.com/get-docker/).

```bash
$ docker -v
```

## Docker Compose

Docker Compose v2 ships with current versions of Docker. Installation instructions can be found [here](https://docs.docker.com/compose/install/).

```bash
$ docker compose version
```

::: info
Some pages in these docs use the older `docker-compose` command. With Compose v2, use `docker compose` instead.
:::

## Java

Only needed to build the Registry from source. Installation instructions for Java 11 can be found [here](https://adoptium.net/).

```bash
$ java -version
```

## NodeJS

Only needed for the Registry CLI, or to run the Credentials services from source. Installation instructions for NodeJS can be found [here](https://nodejs.org/).

```bash
$ node -v
```
