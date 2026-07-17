# Quantum Workforce OS (QWOS)

# User Profiles Entity Specification

**Document ID:** DB-IDENTITY-003

**Entity:** User Profiles

**Table:** `user_profiles`

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `user_profiles` entity stores personal profile information for authenticated users.

Unlike the `users` entity, which manages authentication and security, `user_profiles` contains information used for display, communication, localization, and personalization.

Separating identity from profile information improves maintainability, supports multiple authentication methods, and allows future business domains to reuse profile data without duplication.

---

# 2. Business Responsibilities

The `user_profiles` entity is responsible for:

* Personal identity information
* Display preferences
* Localization preferences
* Profile photo
* Communication preferences
* User interface personalization

---

# 3. Table Name

```text
user_profiles
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity           | Relationship                                                             |
| ------------------------ | ------------------------------------------------------------------------ |
| users                    | One-to-one                                                               |
| organizations            | Many profiles belong to one organization (through the user relationship) |
| employees (future)       | One-to-one                                                               |
| client_contacts (future) | One-to-one                                                               |
| recruiters (future)      | One-to-one                                                               |

---

# 6. Columns

| Column         | Type         | Required | Notes                              |
| -------------- | ------------ | -------- | ---------------------------------- |
| id             | ULID         | Yes      | Primary Key                        |
| tenant_id      | ULID         | Yes      | Tenant ownership                   |
| user_id        | ULID         | Yes      | References `users.id`              |
| first_name     | VARCHAR(100) | Yes      | Given name                         |
| middle_name    | VARCHAR(100) | No       | Optional                           |
| last_name      | VARCHAR(100) | Yes      | Family name                        |
| display_name   | VARCHAR(150) | Yes      | Preferred display name             |
| preferred_name | VARCHAR(100) | No       | Nickname or informal name          |
| avatar_url     | TEXT         | No       | Profile image location             |
| locale         | VARCHAR(10)  | Yes      | e.g. `en-PH`, `en-US`              |
| timezone       | VARCHAR(100) | Yes      | IANA timezone identifier           |
| language       | VARCHAR(20)  | Yes      | Preferred application language     |
| created_at     | TIMESTAMPTZ  | Yes      | UTC                                |
| created_by     | ULID         | No       | User who created the record        |
| updated_at     | TIMESTAMPTZ  | Yes      | UTC                                |
| updated_by     | ULID         | No       | User who last updated the record   |
| deleted_at     | TIMESTAMPTZ  | No       | Soft delete timestamp              |
| deleted_by     | ULID         | No       | User who performed the soft delete |
| version        | INTEGER      | Yes      | Optimistic locking                 |

---

# 7. Validation Rules

* First and last names are required.
* Display name is required and must not exceed 150 characters.
* Locale must use a supported language-region format (e.g. `en-PH`).
* Timezone must be a valid IANA timezone.
* Avatar URL, when provided, must be a valid URL.

---

# 8. Business Rules

* Every user must have exactly one profile.
* Every profile belongs to exactly one user.
* Profile information may be edited without affecting authentication.
* Personal profile data is shared across business domains through references rather than duplication.
* Profile deletion follows the platform's soft-delete policy.

---

# 9. Constraints

| Constraint  | Description                      |
| ----------- | -------------------------------- |
| Primary Key | `id`                             |
| Foreign Key | `user_id → users.id`             |
| Foreign Key | `tenant_id → organizations.id`   |
| Unique      | `user_id` (one profile per user) |

---

# 10. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Unique (`user_id`)
* Index (`display_name`)
* Index (`last_name`)
* Index (`tenant_id`)
* Index (`deleted_at`)

---

# 11. Security Classification

| Column         | Classification |
| -------------- | -------------- |
| first_name     | Confidential   |
| middle_name    | Confidential   |
| last_name      | Confidential   |
| preferred_name | Internal       |
| avatar_url     | Internal       |
| locale         | Internal       |
| timezone       | Internal       |
| language       | Internal       |

Personally identifiable information (PII) should be handled in accordance with organizational privacy policies and applicable regulations.

---

# 12. API Usage

Typical operations include:

* View profile
* Update profile
* Upload avatar
* Change language
* Change timezone
* Update display name

Authentication and authorization remain the responsibility of the `users` entity.

---

# 13. UI Usage

Primary screens:

* My Profile
* User Profile
* Account Settings
* Team Directory
* Employee Overview (future)

Display name and avatar should be used throughout the application where appropriate.

---

# 14. Example Record (Conceptual)

| Field          | Example                    |
| -------------- | -------------------------- |
| id             | 01JXKAB7R4Y5M9N2Q3P8L6T1V0 |
| user_id        | 01JXK9Y8T8K5K6WQ2E7M4J1S9A |
| first_name     | Richard                    |
| middle_name    | Santos                     |
| last_name      | Balabarcon                 |
| display_name   | Richard Balabarcon         |
| preferred_name | Richard                    |
| locale         | en-PH                      |
| timezone       | Asia/Manila                |
| language       | English                    |

---

# 15. Future Enhancements

Future versions may introduce:

* Multiple avatars
* Pronouns (optional and organization-configurable)
* Digital signatures
* Profile completion score
* Contact methods (phones, messaging accounts)
* Addresses (separate domain entity)
* Emergency contacts
* Social links

These enhancements will be implemented through related entities to maintain normalization.

---

# 16. Acceptance Criteria

The `user_profiles` entity is complete when:

* One-to-one relationship with `users` is established.
* Personal information is separated from authentication data.
* Validation rules are documented.
* Constraints and indexes are defined.
* API and UI dependencies are identified.
* Privacy and security considerations are documented.

---

# Summary

The `user_profiles` entity represents the personal aspect of an authenticated user while keeping authentication, authorization, and security concerns within the `users` entity. This separation supports a clean domain model, minimizes data duplication, and prepares Quantum Workforce OS for future HR, CRM, and customer-facing capabilities.
