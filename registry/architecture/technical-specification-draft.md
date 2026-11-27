---
title: "Technical Specification Draft"
description: "Terminology, schemas, configuration, attestation, enrolment, discovery and consent for the Sunbird RC registry."
---

# Technical Specification Draft

Terminology, schemas, configuration, attestation, enrolment, discovery and consent for the Sunbird RC registry.

## Terminology

<table data-search="false"><thead><tr><th width="260">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Data</strong></td><td>Electronic data of any type. It could be simple data or composite data.</td></tr><tr><td><strong>Database</strong></td><td>A software system that stores and manages data.</td></tr><tr><td><strong>Schema</strong></td><td>Machine-readable definition of data.</td></tr><tr><td><strong>Actor (Subject)</strong></td><td>A person, entity or thing that has been identified.</td></tr><tr><td><strong>Transaction / Interaction Data</strong></td><td>Data representing details of an interaction or transaction done among one or more actors within a system.</td></tr><tr><td><strong>SoR (System of Record)</strong></td><td>A software system that is the primary system enabling a specific set of transactions/interactions through a set of workflows and user interfaces. Identities of actors participating in these transactions/interactions may be linked to a registry.</td></tr><tr><td><strong>Registration</strong></td><td>The act of registering or enrolling an actor into a system.</td></tr><tr><td><strong>Claim</strong></td><td>A statement made by an actor which can be verified.</td></tr><tr><td><strong>Attestation</strong></td><td>The act of verifying and authorizing specific data in a digitally signed fashion by an authorized individual/entity (whose identities are typically linked to some other registries).</td></tr><tr><td><strong>Discovery</strong></td><td>The act of finding specific entries in a registry through a search/find mechanism.</td></tr><tr><td><strong>Assertion</strong></td><td>The act of verifying a claim.</td></tr><tr><td><strong>Consent</strong></td><td>Approval given by an actor to another person/system to access the actor's data for purposes of a transaction/interaction.</td></tr><tr><td><strong>Credential</strong></td><td>A digitally represented, verifiable artifact containing a qualification, achievement, milestone, fact, etc., issued to an actor so they can make claims.</td></tr><tr><td><strong>Registry</strong></td><td>An electronic registry is a system acting as a single source of truth. It houses a set of common attributes of the actor in a trustable (attested) and non-repudiable (audited) fashion, under the actor's control — enabling actors to authenticate themselves and make claims about themselves, with their consent, which can be electronically verified by third-party systems.</td></tr><tr><td><strong>Information Provider</strong></td><td>An authorized entity or person who manages a SoR to enable specific transactions/interactions among various actors. Using their systems of record, this entity provides digitally verifiable credentials, documents, certificates, transaction/interaction data, etc. back to actors.</td></tr><tr><td><strong>Information Users</strong></td><td>An entity accessing credentials/data of an actor, with the actor's consent, to make assertions and provide various services/products.</td></tr></tbody></table>

## Workflow

![](/images/screenshot-2021-09-09-at-3-46-52-pm-289047bf.png)

## Schema

All registries have attributes pertaining to the entity or fact in question, whether a person or a thing. A schema defines the structure and constraints of the entity. Sunbird RC uses standard JSON-LD based schemas.

In the example below, `Place` is the concept the registry stores, supporting `name`, `city`, `addressRegion` (state) and `country`.

### Example

```json
{
 "$schema": "http://json-schema.org/draft-07/schema",
 "type": "object",
 "properties": {
   "Place": {
     "$ref": "#/definitions/Place"
   }
 },
 "required": [
   "Place"
 ],
 "title": "Place",
 "definitions": {
   "Place": {
     "$id": "#/properties/Place",
     "type": "object",
     "title": "The Place Schema",
     "required": [
       "name",
       "city",
       "addressRegion",
       "country"
     ],
     "properties": {
       "name": {
         "type": "string"
       },
       "city": {
         "type": "string"
       },
       "addressLocality": {
         "type": "string"
       },
       "addressRegion": {
         "type": "string"
       },
       "country": {
         "type": "string"
       },
       "postalCode": {
         "type": "string"
       },
       "contact": {
         "type": "string"
       }
     }
   }
 }}
```

## Configuration

In addition to JSON-LD specific data types, Sunbird RC supports various extension configurations under `_osConfig`. Access, indexing, primary keys, etc. are configurable using schema configuration.

### Property data types and restrictions

Supported types:

* **String** — Unicode text; additional regular-expression restrictions can be applied.
* **Enum** — a restricted list of values.
* **Number** — numeric data.

### List of attributes

Collections of data values are also supported, as multiple values might represent an entity property — for example, subjects taught: `["english", "science", "mathematics"]`

### Visibility scope

There are three types of visibility on attributes:

<table data-search="false"><thead><tr><th width="220">Visibility</th><th>Who can access it</th></tr></thead><tbody><tr><td><strong>Public</strong></td><td>Available in discovery by default — no permission or authorization is needed.</td></tr><tr><td><strong>Private</strong> (<code>privateFields</code>)</td><td>Accessible by the owner by default; third parties can access the field with consent.</td></tr><tr><td><strong>Internal</strong></td><td>System fields that only serve internal functionality. These can never be accessed by any actor in the system.</td></tr></tbody></table>

### Primary keys for entities

Primary keys from the domain space help enforce uniqueness of information and make it easily accessible. Use `uniqueIndexFields` to configure them.

```json
"uniqueIndexFields": [ "identityValue", ... ]
```

### Index field set

Indexes help with faster access to information. Index fields can be configured based on the usage context:

```json
"indexFields": ["phoneNumber", ... ],
```

### Validation extensions

JSON-LD schema allows defining basic type constraints such as numeric type, text or a list of items. It also allows a list of possible values for given attributes (enum), and regular-expression based constraints for the value.

### Schema access API

Sunbird RC supports the following API for accessing schemas:

```http
GET /api/docs/{entityName}.json
```

The Swagger document is accessible at:

```http
GET /api/docs/swagger.json
```

## Attestation

### Configuration

Attestation on a given set of fields is configurable with schema configuration. Below is an example of an attestation requirement using DSL:

```json
 "attestationPolicies": [
 {
     "property": "experience/\[\]",
     "paths": [ "experience" ],
     "attestorEntity": "Institute",
     "conditions": "\(ATTESTOR\#$.instituteName\#.contains\(REQUESTER\#$.institute\#\)\)"
 },
  ...
 ]
```

### Attestation types

Attestation requirements will be mixed: some need human verification, while others can be completely digital. To begin with, registries can allow both manual and automatic attestation. For example, a teacher rewarding and attesting grades can be a manual activity, while an identity claim can be attested digitally by an identity provider like Aadhaar.

:::: tabs
== Manual attestation

Manual attestation may need a workflow. By default, the registry supports raising a claim against a pre-configured attestation requirement. The claim is routed to the appropriate authority/role based on the configuration. Once the claim is approved or rejected, the respective fields in the claim show as verified or invalid.

The attestor is controlled with the `attestorEntity` configuration.

== Automated attestation

Digital registries can interoperate, sharing trusted claims and information among themselves. To do so, a claim can be routed to an automated registry verifier, which proxies for another registry and takes care of verification and attestation. Such attestation can be time-bound or one-time.

**Example:** An identity registry can be used to prove the identity of a subject without manual verification. A mobile OTP-based consent flow can verify the identity and mark the subject's name as verified. Eventually, certificates issued by educational institutions can also be verified digitally.
::::

### Attestation API

```http
POST /api/v1/{entityName}/{entityId}/attest/{propertyID}
{
  "action":"GRANT_CLAIM"
  ...
}
```

### Custom extensions

The attestation workflow might need custom stages and transition rules based on the use case. Attestation is extensible, so you can add or customize these workflows and add custom rules as needed.

## Enrolment / signup

### Sign up

The enrolment/signup API supports self-signup and bulk invites to register in the registry.

::: info
One of the principles of the registry is to avoid loading stale data from databases, and instead give subjects control — letting them participate in registration and manage their own data, rather than someone else managing it for them.
:::

```http
POST /api/v1/{entityName}/invite
{
"name":"Suresh",
"email":"suresh@example.com"
}
```

### Update information

```http
PATCH /api/v1/{entityName}/{entityId}
{
  "fieldPaths":["/name"]
}
```

## Discovery

### Search API

```http
POST /api/v1/search
{
  "email":"suresh@example.com"
}
```

### Directory

Example: pincode lookup

```http
POST /api/v1/search { "state":"Karnataka" }
```

## Consent API

### Authentication flow

![](/images/screenshot-2021-09-09-at-3-48-47-pm-1f1d6e72.png)

### Request scopes and sharing attributes

```http
GET /partner/api/v1/{entityName}
```

## Use cases

* Building a blood donor registry
* Building a simple pincode directory service
* Education registry
* Immunization
* Authentication and consent usage in a learning application
