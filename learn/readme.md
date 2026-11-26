---
title: "Overview"
description: "Build live, reusable and trustworthy registries and verifiable credentials — with configuration, not code."
---

# Overview

Build live, reusable and trustworthy registries and verifiable credentials — with configuration, not code.

Every digital platform runs on **master data** — structured, validated records about people, entities and things. Increasingly, this data lives in electronic registries with open APIs, so other systems can use attested, authenticated data instead of relying on paper-based checks. That lowers the cost of trust, especially when claims about people and entities need to be verified.

## The challenge

As registries scale, most of them run into the same three problems:

<table data-view="cards"><thead><tr><th></th><th></th><th data-type="image"></th></tr></thead><tbody><tr><td><strong>Live</strong></td><td>Data goes stale fast. Contact details, credentials and records change constantly, and re-collecting them is slow and expensive.</td><td></td></tr><tr><td><strong>Reusable</strong></td><td>Data trapped in one system can't be reused by another, so every department repeats the same collection and maintenance work.</td><td></td></tr><tr><td><strong>Trustworthy</strong></td><td>Data without a digital signature or attestation can't be trusted elsewhere. A CSV exported from a portal offers no guarantee it's authentic or unedited.</td><td></td></tr></tbody></table>

What's needed is an interoperable, unified registry infrastructure that makes registries live, reusable and trustworthy at once — a single source of truth that other systems can rely on without re-verifying it.

## What is Sunbird RC?

**Sunbird RC (Registry and Credentials)** is a low-code, open-source package for building electronic registries and issuing verifiable credentials. It has two components, which can be used on their own or together:

* **Registry** — builds an authoritative source of record for people, entities and things.
* **Credentials** — issues, manages and revokes W3C verifiable credentials from a trusted data source.

Instead of writing custom code, you describe your registry and credentials through configuration. Sunbird RC then generates the APIs, attestation and consent flows, and credential issuance and verification needed around them.

::: tip
**Open source and free to use.** Sunbird RC is [MIT-licensed](https://opensource.org/license/MIT) and listed as a global Digital Public Good in the [Digital Public Goods Alliance (DPGA) registry](https://digitalpublicgoods.net/registry/). It is the core engine behind DIVOC (vaccination and health credentialing). See [Adopters](/learn/adopters) for other implementations and their status.
:::

## A registry is an authoritative source, not just a database

A Sunbird RC registry is more than a store with CRUD and search APIs. It is the place other systems go to for the **authoritative version** of a record:

* **Owned by an authority.** The body responsible for the data — a ministry, a council, an institution — defines the schema and the rules for who can create, change and see each record.
* **Attested.** Claims can be checked by attesters before they are accepted, through configurable single- or multi-level attestation workflows.
* **Signed.** Records can be digitally signed, so anyone relying on them can confirm where they came from and that they haven't been altered.
* **Access-controlled.** Field-level privacy and consent decide who can see what.
* **Reused, not re-collected.** Other systems read from the registry through its APIs instead of collecting and maintaining their own copies.

The APIs are how systems use the registry; the trust in the data is what makes it authoritative. For more on the difference, see [Registry vs Database](/help/comprehensive-overview-electronic-registries-and-verifiable-credentials/electronic-registries/registry-vs-database).

## From data source to verifier

A verifiable credential carries trusted data from where it is held to wherever it needs to be checked:

1. **Data source** — the authoritative record. This can be a Sunbird RC Registry, or any existing system of record you already run.
2. **Credential** — the Credentials component issues and signs a verifiable credential from that record.
3. **Holder** — the person or organisation the credential is about keeps it in a wallet or other digital storage they control.
4. **Verifier** — an employer, agency or service checks the credential's signature and status, without calling the issuer.

Because the Credentials component does not depend on where the data lives, you can issue credentials from an existing database or registry without moving it into Sunbird RC. If you also use the Registry component, the two connect directly. See [Workflows](/learn/readme/workflows) for each step in detail.

## Watch: What is Sunbird RC?

Hear Dr Pramod Varma, CTO of EkStep Foundation, explain the thinking behind Sunbird RC.

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/HsQK5uSUnDk" title="What is Sunbird RC? by Dr Pramod Varma" allowfullscreen loading="lazy"></iframe></div>
<p class="embed-caption">What is Sunbird RC? by Dr Pramod Varma</p>

## What Sunbird RC provides

<table data-search="false"><thead><tr><th width="220">Feature</th><th>What it does</th></tr></thead><tbody><tr><td><strong>Master data store</strong></td><td>Model entities with flexible schemas (JSON/JSON-LD); attach validation, lifecycle and relationship rules</td></tr><tr><td><strong>Data operations</strong></td><td>Secure, API-driven CRUD; open APIs for publishing, access, and key-value or attribute search</td></tr><tr><td><strong>Data protection</strong></td><td>Encryption, masking, pluggable custom encryption services, audit trails and logging</td></tr><tr><td><strong>Single source of truth</strong></td><td>Digital signatures for trust and non-repudiation across every registry record</td></tr><tr><td><strong>Your choice of database</strong></td><td>Out-of-the-box adapters for multiple databases, including Postgres and graph DBs like Neo4j</td></tr><tr><td><strong>Modular and configurable</strong></td><td>Tailor the platform to your needs; supports multiple languages and multi-cloud deployment</td></tr><tr><td><strong>Observability</strong></td><td>Telemetry and analytics for monitoring system health, with audit logs to catch issues early</td></tr></tbody></table>

## Explore further

* [Why do we need Sunbird RC?](/learn/readme/why-do-we-need-sunbird-rc)
* [Core Capabilities](/learn/readme/core-capabilities)
* [Workflows](/learn/readme/workflows)
* [What Sunbird RC is and what it's not](/learn/readme/what-sunbird-rc-is-and-what-its-not)
* [Possibilities](/learn/readme/possibilities)
