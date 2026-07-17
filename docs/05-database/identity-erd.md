# Quantum Workforce OS (QWOS)

# Identity Domain – Entity Relationship Design (ERD)

**Document ID:** DB-IDENTITY-001

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

This document defines the conceptual Entity Relationship Design (ERD) for the Identity Domain.

It identifies the entities, relationships, ownership boundaries, and data governance rules that support authentication, authorization, user identity, and secure access across Quantum Workforce OS.

This document is conceptual and precedes the physical PostgreSQL schema.

---

# 2. Design Principles

The Identity Domain follows these principles:

* Multi-tenant architecture
* Soft delete by default
* Audit fields on every table
* ULID primary keys
* Normalized data model (Third Normal Form)
* Role-Based Access Control (RBAC)
* No duplicated identity data

---

# 3. Core Entities

The Identity Domain consists of the following entities:

* Organization
* User
* Role
* Permission
* Role Permission
* User Role
* Session
* Refresh Token
* Login History
* Invitation
* Password Reset
* Email Verification
* Security Policy

These entities collectively manage authentication, authorization, identity lifecycle, and security policies.

---

# 4. Entity Relationships

```text
Organization
    │
    ├──────────────┐
    │              │
    ▼              ▼
 User         Security Policy
    │
    ├──────────────┐
    │              │
    ▼              ▼
User Role      Session
    │              │
    ▼              ▼
 Role      Refresh Token
    │
    ▼
Role Permission
    │
    ▼
Permission

User
 │
 ├──────────────┐
 │              │
 ▼              ▼
Invitation   Login History

User
 │
 ▼
Password Reset

User
 │
 ▼
Email Verification
```

---

# 5. Relationship Definitions

## Organization → User

Relationship:

One Organization

↓

Many Users

Each user belongs to one primary organization in Version 1.0.

Future versions may support membership in multiple organizations.

---

## User → User Role

One User

↓

Many User Roles

Users may hold multiple roles.

Example:

* HR Manager
* Recruiter
* Executive Assistant

---

## Role → Permission

Many-to-Many

Implemented through:

Role Permission

---

## User → Session

One User

↓

Many Sessions

Supports:

* Multiple devices
* Mobile
* Browser sessions

---

## User → Refresh Token

One User

↓

Many Refresh Tokens

Each login creates a new refresh token.

---

## User → Login History

One User

↓

Many Login Events

Used for:

* Security
* Auditing
* Analytics

---

## User → Password Reset

One User

↓

Many Password Reset Requests

Historical requests are retained.

---

## User → Email Verification

One User

↓

Many Verification Records

Supports:

* Initial verification
* Email change verification

---

# 6. Aggregate Roots

Identity Aggregate

Owns:

* User
* Session
* Refresh Token
* Login History

Authorization Aggregate

Owns:

* Role
* Permission
* Role Permission
* User Role

Security Aggregate

Owns:

* Security Policy
* Password Reset
* Email Verification

---

# 7. Shared Fields

Every entity shall contain:

* id (ULID)
* tenant_id
* created_at
* updated_at
* created_by
* updated_by
* deleted_at

These fields provide:

* Auditability
* Multi-tenancy
* Soft deletion

---

# 8. Data Ownership

| Entity             | Owner    |
| ------------------ | -------- |
| User               | Identity |
| Role               | Identity |
| Permission         | Identity |
| Session            | Identity |
| Refresh Token      | Identity |
| Invitation         | Identity |
| Login History      | Identity |
| Password Reset     | Identity |
| Email Verification | Identity |
| Security Policy    | Identity |

No other domain may modify these entities directly.

---

# 9. Future Entities

Future releases may introduce:

* API Key
* Service Account
* OAuth Provider
* Device Registration
* MFA Device
* Trusted Device
* Security Event
* Access Policy
* SSO Configuration

---

# 10. ERD Governance Rules

The following rules apply to every Identity entity:

* Primary key must use ULID.
* Audit fields are mandatory.
* Soft delete is mandatory.
* No duplicated business data.
* Foreign keys enforce referential integrity.
* Sensitive values are encrypted or hashed where appropriate.

---

# 11. Summary

The Identity Domain ERD establishes the conceptual data model for authentication, authorization, and identity management within Quantum Workforce OS.

This design provides a secure, scalable, and extensible foundation for implementing enterprise-grade identity services while maintaining strict tenant isolation and complete auditability.
