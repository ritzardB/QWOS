# Quantum Workforce OS (QWOS)

# Role Permissions Entity Specification

**Document ID:** DB-IDENTITY-006

**Entity:** Role Permissions

**Table:** `role_permissions`

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `role_permissions` entity defines the relationship between roles and permissions.

Rather than acting as a simple junction table, it represents the assignment of a specific permission to a specific role and supports auditing, lifecycle management, and future authorization enhancements.

---

# 2. Business Responsibilities

The `role_permissions` entity is responsible for:

* Assigning permissions to roles.
* Tracking permission assignments.
* Supporting temporary permission assignments.
* Maintaining audit history.
* Enabling future policy extensions.

---

# 3. Table Name

```text
role_permissions
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity | Relationship |
| -------------- | ------------ |
| roles          | Many-to-one  |
| permissions    | Many-to-one  |

Each record links exactly one role to one permission.

---

# 6. Columns

| Column          | Type        | Required | Notes                              |
| --------------- | ----------- | -------- | ---------------------------------- |
| id              | ULID        | Yes      | Primary Key                        |
| tenant_id       | ULID        | Yes      | Tenant ownership                   |
| role_id         | ULID        | Yes      | References `roles.id`              |
| permission_id   | ULID        | Yes      | References `permissions.id`        |
| is_enabled      | BOOLEAN     | Yes      | Default: true                      |
| granted_at      | TIMESTAMPTZ | Yes      | UTC                                |
| granted_by      | ULID        | No       | User who granted the permission    |
| effective_from  | TIMESTAMPTZ | No       | Optional activation date           |
| effective_until | TIMESTAMPTZ | No       | Optional expiration date           |
| notes           | TEXT        | No       | Administrative notes               |
| created_at      | TIMESTAMPTZ | Yes      | UTC                                |
| created_by      | ULID        | No       | User who created the record        |
| updated_at      | TIMESTAMPTZ | Yes      | UTC                                |
| updated_by      | ULID        | No       | User who last updated the record   |
| deleted_at      | TIMESTAMPTZ | No       | Soft delete timestamp              |
| deleted_by      | ULID        | No       | User who performed the soft delete |
| version         | INTEGER     | Yes      | Optimistic locking                 |

---

# 7. Validation Rules

* `role_id` and `permission_id` are required.
* Duplicate active role-permission assignments are not allowed.
* If both dates are present, `effective_until` must be later than `effective_from`.
* Disabled assignments remain in the database for audit purposes.

---

# 8. Business Rules

* A role may have many permissions.
* A permission may belong to many roles.
* Only enabled assignments are considered during authorization.
* Future-dated assignments are inactive until their start date.
* Expired assignments are ignored by the authorization engine.
* Removing access should normally disable or soft-delete the assignment rather than physically deleting it.

---

# 9. Constraints

| Constraint  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| Primary Key | `id`                                                         |
| Foreign Key | `role_id → roles.id`                                         |
| Foreign Key | `permission_id → permissions.id`                             |
| Foreign Key | `tenant_id → organizations.id`                               |
| Unique      | `(tenant_id, role_id, permission_id)` for active assignments |
| Check       | `effective_until > effective_from` when both values exist    |

---

# 10. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Index (`tenant_id`)
* Index (`role_id`)
* Index (`permission_id`)
* Composite Index (`tenant_id`, `role_id`)
* Composite Index (`tenant_id`, `permission_id`)
* Index (`is_enabled`)
* Index (`deleted_at`)

---

# 11. Security Classification

| Column        | Classification |
| ------------- | -------------- |
| role_id       | Internal       |
| permission_id | Internal       |
| granted_by    | Restricted     |
| notes         | Internal       |

Changes to role-permission assignments should be audited and restricted to authorized administrators.

---

# 12. API Usage

Typical operations include:

* Assign permission to role
* Remove permission from role
* Enable assignment
* Disable assignment
* List permissions for a role
* List roles using a permission

---

# 13. UI Usage

Primary screens:

* Role Details
* Permission Assignment
* Security Administration

The UI should support searching, filtering, and grouping permissions by domain and category.

---

# 14. Example Record

| Field           | Example                    |
| --------------- | -------------------------- |
| role_id         | HR Manager                 |
| permission_id   | workforce.employees.update |
| is_enabled      | true                       |
| granted_at      | 2026-07-13T10:30:00Z       |
| effective_from  | 2026-07-15T00:00:00Z       |
| effective_until | *(null)*                   |

---

# 15. Future Enhancements

Future versions may support:

* Conditional permission assignments
* Approval workflows
* Policy-based overrides
* Delegated administration
* Attribute-Based Access Control (ABAC)
* Just-In-Time (JIT) access

The current structure is designed to accommodate these capabilities without major schema changes.

---

# 16. Acceptance Criteria

The `role_permissions` entity is complete when:

* Relationships between roles and permissions are documented.
* Validation rules and constraints are defined.
* Effective dating is supported.
* Audit information is captured.
* API and UI dependencies are identified.
* Security considerations are documented.

---

# Summary

The `role_permissions` entity is the central assignment layer of the RBAC model. By treating permission assignments as first-class business records rather than simple join rows, Quantum Workforce OS gains stronger auditability, greater flexibility, and a clear path toward advanced authorization capabilities.
