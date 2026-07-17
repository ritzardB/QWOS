# Quantum Workforce OS (QWOS)

# Identity Domain Entity Relationship Diagram (ERD)

**Document ID:** DB-IDENTITY-ERD-001

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

This document provides a visual and conceptual representation of the Identity Domain database model.

The Entity Relationship Diagram (ERD) illustrates how authentication, authorization, user management, and security entities relate to one another.

It serves as the primary reference for database implementation, ORM model generation, API development, and onboarding new developers.

---

# 2. Identity Domain Overview

The Identity Domain is composed of four logical groups:

## Core Identity

* Users
* User Profiles

## Authorization

* Roles
* Permissions
* User Roles
* Role Permissions

## Authentication Activities

* Sessions
* Refresh Tokens
* Login History

## Security

* Password Resets
* Email Verifications
* Invitations
* Security Policies

---

# 3. High-Level ER Diagram

```text
                                    ORGANIZATIONS
                                           │
                                           │ 1
                                           │
                                           ▼
                                       USERS
                                   (Identity Root)
                                           │
                         ┌─────────────────┼─────────────────┐
                         │                 │                 │
                       1 │               1 │               1 │
                         ▼                 ▼                 ▼
                USER_PROFILES         USER_ROLES        SESSIONS
                         │                 │                 │
                         │                 │                 ├─────────────► REFRESH_TOKENS
                         │                 │
                         │                 ▼
                         │               ROLES
                         │                 │
                         │                 ▼
                         │        ROLE_PERMISSIONS
                         │                 │
                         │                 ▼
                         │           PERMISSIONS
                         │
                         ├──────────────► LOGIN_HISTORY
                         │
                         ├──────────────► PASSWORD_RESETS
                         │
                         ├──────────────► EMAIL_VERIFICATIONS
                         │
                         └──────────────► INVITATIONS
```

---

# 4. Relationship Summary

## Users ↔ User Profiles

Relationship:

One-to-One

Purpose:

Separates authentication data from personal profile information.

---

## Users ↔ User Roles

Relationship:

One-to-Many

Purpose:

Allows multiple active role assignments per user.

---

## Roles ↔ Role Permissions

Relationship:

One-to-Many

Purpose:

Associates roles with permission assignments.

---

## Permissions ↔ Role Permissions

Relationship:

One-to-Many

Purpose:

Defines which permissions belong to each role.

---

## Users ↔ Sessions

Relationship:

One-to-Many

Purpose:

Supports multiple concurrent authenticated sessions.

---

## Sessions ↔ Refresh Tokens

Relationship:

One-to-Many

Purpose:

Supports secure token refresh without requiring users to log in again.

---

## Users ↔ Login History

Relationship:

One-to-Many

Purpose:

Provides an immutable audit trail of authentication activity.

---

## Users ↔ Password Resets

Relationship:

One-to-Many

Purpose:

Maintains a history of password reset requests.

---

## Users ↔ Email Verifications

Relationship:

One-to-Many

Purpose:

Tracks email verification events for account activation and future email changes.

---

## Users ↔ Invitations

Relationship:

One-to-Many

Purpose:

Records invitation workflows for onboarding users into organizations.

---

# 5. Entity Classification

## Core Business Entities

| Entity        | Purpose                             |
| ------------- | ----------------------------------- |
| users         | Digital identity and authentication |
| user_profiles | Personal profile information        |
| roles         | Business responsibilities           |
| permissions   | Atomic authorization rules          |

---

## Assignment Entities

| Entity           | Purpose                      |
| ---------------- | ---------------------------- |
| user_roles       | Assigns roles to users       |
| role_permissions | Assigns permissions to roles |

---

## Activity Entities

| Entity              | Purpose                       |
| ------------------- | ----------------------------- |
| sessions            | Active authenticated sessions |
| refresh_tokens      | Session renewal               |
| login_history       | Authentication audit trail    |
| password_resets     | Password recovery history     |
| email_verifications | Email verification history    |

---

## Configuration Entities

| Entity            | Purpose                           |
| ----------------- | --------------------------------- |
| security_policies | Tenant-specific security settings |
| invitations       | User onboarding process           |

---

# 6. Aggregate Boundaries

The Identity Aggregate consists of:

```text
Identity

├── Users
├── User Profiles
├── User Roles
├── Roles
├── Permissions
├── Role Permissions
├── Sessions
├── Refresh Tokens
├── Login History
├── Password Resets
├── Email Verifications
├── Invitations
└── Security Policies
```

Each entity belongs exclusively to the Identity Domain.

Other domains interact through APIs rather than directly modifying these tables.

---

# 7. Cardinality Summary

| Parent       | Child               | Cardinality |
| ------------ | ------------------- | ----------- |
| Organization | Users               | 1 : Many    |
| Users        | User Profiles       | 1 : 1       |
| Users        | User Roles          | 1 : Many    |
| Roles        | User Roles          | 1 : Many    |
| Roles        | Role Permissions    | 1 : Many    |
| Permissions  | Role Permissions    | 1 : Many    |
| Users        | Sessions            | 1 : Many    |
| Sessions     | Refresh Tokens      | 1 : Many    |
| Users        | Login History       | 1 : Many    |
| Users        | Password Resets     | 1 : Many    |
| Users        | Email Verifications | 1 : Many    |
| Users        | Invitations         | 1 : Many    |

---

# 8. Design Principles

The Identity Domain follows these principles:

* Identity is separated from personal profile data.
* Authorization is implemented using Role-Based Access Control (RBAC).
* Assignments are modeled as business entities.
* Authentication activities are immutable whenever practical.
* Soft deletes preserve historical data.
* Every entity includes audit fields.
* Multi-tenancy is enforced across all business entities.

---

# 9. Implementation Notes

This ERD serves as the blueprint for:

* PostgreSQL schema generation
* SQLAlchemy ORM models
* Alembic migrations
* FastAPI endpoints
* Pydantic schemas
* TypeScript interfaces
* React authentication flows
* Automated tests

All implementation artifacts should remain consistent with this model.

---

# 10. Summary

The Identity Domain ERD provides a clear, maintainable, and scalable representation of the authentication and authorization model within Quantum Workforce OS.

By separating identity, profile information, authorization, and authentication activities into distinct entities, the platform establishes a strong foundation for secure, enterprise-grade identity management while remaining flexible for future enhancements.
