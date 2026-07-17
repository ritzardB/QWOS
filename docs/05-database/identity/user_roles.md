# Quantum Workforce OS (QWOS)

# User Roles Entity Specification

**Document ID:** DB-IDENTITY-007

**Entity:** User Roles

**Table:** `user_roles`

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `user_roles` entity assigns one or more roles to individual users.

Rather than storing a role directly on the `users` entity, this design supports multiple concurrent roles, temporary assignments, delegated responsibilities, and future authorization enhancements while maintaining a complete audit trail.

---

# 2. Business Responsibilities

The `user_roles` entity is responsible for:

* Assigning roles to users.
* Supporting multiple active roles.
* Tracking role assignment history.
* Supporting temporary assignments.
* Identifying a primary role.
* Recording assignment metadata.

---

# 3. Table Name

```text
user_roles
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity | Relationship |
| -------------- | ------------ |
| users          | Many-to-one  |
| roles          | Many-to-one  |

Each record links one user to one role.

---

# 6. Columns

| Column            | Type        | Required | Notes                              |
| ----------------- | ----------- | -------- | ---------------------------------- |
| id                | ULID        | Yes      | Primary Key                        |
| tenant_id         | ULID        | Yes      | Organization ownership             |
| user_id           | ULID        | Yes      | References `users.id`              |
| role_id           | ULID        | Yes      | References `roles.id`              |
| is_primary        | BOOLEAN     | Yes      | Indicates the user's primary role  |
| is_enabled        | BOOLEAN     | Yes      | Default: true                      |
| assigned_at       | TIMESTAMPTZ | Yes      | UTC                                |
| assigned_by       | ULID        | No       | User who assigned the role         |
| effective_from    | TIMESTAMPTZ | No       | Optional start date                |
| effective_until   | TIMESTAMPTZ | No       | Optional end date                  |
| assignment_reason | TEXT        | No       | Business justification             |
| created_at        | TIMESTAMPTZ | Yes      | UTC                                |
| created_by        | ULID        | No       | User who created the record        |
| updated_at        | TIMESTAMPTZ | Yes      | UTC                                |
| updated_by        | ULID        | No       | User who last updated the record   |
| deleted_at        | TIMESTAMPTZ | No       | Soft delete timestamp              |
| deleted_by        | ULID        | No       | User who performed the soft delete |
| version           | INTEGER     | Yes      | Optimistic locking                 |

---

# 7. Validation Rules

* `user_id` is required.
* `role_id` is required.
* A user cannot have duplicate active assignments to the same role.
* A user may have only one primary active role per tenant.
* If both effective dates are provided, `effective_until` must be later than `effective_from`.

---

# 8. Business Rules

* Users may hold multiple active roles.
* Only enabled and currently effective assignments participate in authorization.
* Every active user should have one primary role.
* System roles may only be assigned by authorized administrators.
* Removing a role should normally disable or soft-delete the assignment rather than physically deleting it.

---

# 9. Constraints

| Constraint  | Description                                               |
| ----------- | --------------------------------------------------------- |
| Primary Key | `id`                                                      |
| Foreign Key | `tenant_id → organizations.id`                            |
| Foreign Key | `user_id → users.id`                                      |
| Foreign Key | `role_id → roles.id`                                      |
| Unique      | `(tenant_id, user_id, role_id)` for active assignments    |
| Check       | `effective_until > effective_from` when both values exist |

---

# 10. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Index (`tenant_id`)
* Index (`user_id`)
* Index (`role_id`)
* Composite Index (`tenant_id`, `user_id`)
* Composite Index (`tenant_id`, `role_id`)
* Index (`is_primary`)
* Index (`is_enabled`)
* Index (`deleted_at`)

---

# 11. Security Classification

| Column            | Classification |
| ----------------- | -------------- |
| user_id           | Internal       |
| role_id           | Internal       |
| assigned_by       | Restricted     |
| assignment_reason | Internal       |

Role assignments affect authorization and must be auditable.

---

# 12. API Usage

Typical operations include:

* Assign role to user
* Remove role from user
* Set primary role
* Enable or disable role assignment
* List user roles
* List users assigned to a role

---

# 13. UI Usage

Primary screens:

* User Details
* User Security
* Role Assignment
* Organization Administration

The interface should clearly distinguish the primary role from secondary roles.

---

# 14. Example Record

| Field             | Example                    |
| ----------------- | -------------------------- |
| user_id           | Richard Balabarcon         |
| role_id           | HR Manager                 |
| is_primary        | true                       |
| is_enabled        | true                       |
| assigned_at       | 2026-07-13T11:00:00Z       |
| assignment_reason | Initial organization setup |

---

# 15. Future Enhancements

Future versions may support:

* Delegated role assignments
* Approval workflows
* Scheduled role activation
* Automatic role expiration
* Emergency ("break glass") access
* Separation of duties validation

The current structure is designed to accommodate these features without major schema changes.

---

# 16. Acceptance Criteria

The `user_roles` entity is complete when:

* Users can have multiple roles.
* A primary role can be identified.
* Temporary assignments are supported.
* Validation rules and constraints are defined.
* Audit information is captured.
* API and UI dependencies are identified.

---

# Summary

The `user_roles` entity connects authenticated users to the roles that define their permissions. By supporting multiple assignments, effective dates, and auditability, it provides a flexible authorization model suitable for organizations of different sizes while preserving a clear upgrade path for future security capabilities.
