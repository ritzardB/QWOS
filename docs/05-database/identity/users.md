# Quantum Workforce OS (QWOS)

# Users Entity Specification

**Document ID:** DB-IDENTITY-002

**Entity:** Users

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `users` entity represents every authenticated identity within Quantum Workforce OS.

It stores authentication credentials, account status, and security-related information.

Personal profile information is stored separately in the `user_profiles` entity.

This separation allows authentication concerns to evolve independently from personal profile data.

---

# 2. Business Responsibilities

The `users` entity is responsible for:

* User authentication
* Identity management
* Account lifecycle
* Email verification status
* Login eligibility
* Security policies
* Tenant ownership

---

# 3. Table Name

```text
users
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity      | Relationship                                        |
| ------------------- | --------------------------------------------------- |
| organizations       | Many users belong to one organization (Version 1.0) |
| user_profiles       | One-to-one                                          |
| user_roles          | One-to-many                                         |
| sessions            | One-to-many                                         |
| login_history       | One-to-many                                         |
| password_resets     | One-to-many                                         |
| email_verifications | One-to-many                                         |
| invitations         | One-to-many (created or accepted)                   |

---

# 6. Columns

| Column                | Type         | Required    | Notes                                                         |
| --------------------- | ------------ | ----------- | ------------------------------------------------------------- |
| id                    | ULID         | Yes         | Primary Key                                                   |
| tenant_id             | ULID         | Yes         | Organization ownership                                        |
| email                 | VARCHAR(255) | Yes         | Unique within tenant (or globally if platform policy changes) |
| password_hash         | TEXT         | Conditional | Nullable for future SSO/passwordless accounts                 |
| account_status        | ENUM         | Yes         | Pending, Active, Locked, Suspended, Disabled                  |
| email_verified_at     | TIMESTAMPTZ  | No          | Null until verified                                           |
| last_login_at         | TIMESTAMPTZ  | No          | Updated after successful login                                |
| failed_login_attempts | INTEGER      | Yes         | Default: 0                                                    |
| password_changed_at   | TIMESTAMPTZ  | No          | Tracks password rotation                                      |
| created_at            | TIMESTAMPTZ  | Yes         | UTC                                                           |
| created_by            | ULID         | No          | User who created the account                                  |
| updated_at            | TIMESTAMPTZ  | Yes         | UTC                                                           |
| updated_by            | ULID         | No          | User who last updated the account                             |
| deleted_at            | TIMESTAMPTZ  | No          | Soft delete timestamp                                         |
| deleted_by            | ULID         | No          | User who performed the soft delete                            |
| version               | INTEGER      | Yes         | Optimistic locking                                            |

---

# 7. Validation Rules

* Email address is required.
* Email must follow RFC-compliant formatting.
* Passwords are never stored in plain text.
* Passwords must be hashed using the approved password hashing algorithm (implementation documented separately).
* `failed_login_attempts` cannot be negative.
* `account_status` must contain a valid enum value.
* All timestamps are stored in UTC.

---

# 8. Business Rules

* Every user belongs to exactly one tenant in Version 1.0.
* Every user must have one associated `user_profiles` record.
* A user cannot authenticate unless the account status is **Active**.
* Users with **Locked** or **Suspended** status cannot start new sessions.
* Soft-deleted users remain available for audit purposes but cannot authenticate.
* Email verification is required before first login unless an administrator explicitly activates the account.

---

# 9. Constraints

| Constraint  | Description                    |
| ----------- | ------------------------------ |
| Primary Key | `id`                           |
| Foreign Key | `tenant_id → organizations.id` |
| Unique      | `(tenant_id, email)`           |
| Check       | `failed_login_attempts >= 0`   |
| Not Null    | Required fields only           |

---

# 10. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Unique (`tenant_id`, `email`)
* Index (`account_status`)
* Index (`last_login_at`)
* Index (`deleted_at`)
* Index (`created_at`)

Additional indexes should be introduced only after reviewing query performance.

---

# 11. Security Classification

| Column                | Classification |
| --------------------- | -------------- |
| email                 | Confidential   |
| password_hash         | Restricted     |
| failed_login_attempts | Restricted     |
| last_login_at         | Internal       |
| account_status        | Internal       |

Restricted fields require elevated access controls and must never be exposed in API responses unless explicitly required.

---

# 12. API Usage

Typical operations include:

* Register user
* Activate account
* Authenticate
* Change password
* Lock account
* Unlock account
* Disable account
* Reset password

The API specification will define request and response models separately.

---

# 13. UI Usage

Primary screens:

* Login
* User Administration
* Invite User
* User Details
* Security Settings
* Account Status Management

The UI should never display or expose sensitive credential data.

---

# 14. Example Record (Conceptual)

| Field                 | Example                                           |
| --------------------- | ------------------------------------------------- |
| id                    | 01JXK9Y8T8K5K6WQ2E7M4J1S9A                        |
| tenant_id             | 01JXK9A8D7F5H3M2P8Q1R6S4T9                        |
| email                 | [richard@example.com](mailto:richard@example.com) |
| account_status        | Active                                            |
| email_verified_at     | 2026-07-13T08:30:00Z                              |
| last_login_at         | 2026-07-13T09:15:00Z                              |
| failed_login_attempts | 0                                                 |

---

# 15. Future Enhancements

Future versions may support:

* Multiple email addresses
* Passwordless authentication
* External identity providers (Google, Microsoft, Apple)
* Single Sign-On (SSO)
* Service accounts
* API-only users
* Device trust
* Risk-based authentication

The current structure has been designed to support these capabilities with minimal schema changes.

---

# 16. Acceptance Criteria

The `users` entity is complete when:

* The table definition complies with DB-000.
* All required constraints and indexes are documented.
* Business rules are approved.
* Relationships are defined.
* API and UI dependencies are identified.
* Security classifications are assigned.
* The PostgreSQL schema can be generated directly from this specification.

---

# Summary

The `users` entity serves as the central authentication record within the Identity Domain. It focuses exclusively on identity and security concerns while delegating personal information to the `user_profiles` entity. This separation improves maintainability, supports future authentication methods, and aligns with enterprise SaaS design practices.
