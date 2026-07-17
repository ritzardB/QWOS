# Quantum Workforce OS (QWOS)

# Roles Entity Specification

**Document ID:** DB-IDENTITY-004

**Entity:** Roles

**Table:** `roles`

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `roles` entity defines collections of permissions that can be assigned to users.

A role represents a business responsibility rather than a person. Users receive permissions through one or more assigned roles.

This design simplifies permission management, supports organizational flexibility, and aligns with Role-Based Access Control (RBAC) principles.

---

# 2. Business Responsibilities

The `roles` entity is responsible for:

* Defining reusable permission groups.
* Supporting tenant-specific authorization.
* Organizing permissions into meaningful business responsibilities.
* Enabling configurable access control.

Roles do not directly enforce security. Authorization decisions are based on the permissions associated with assigned roles.

---

# 3. Table Name

```text
roles
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity   | Relationship                                   |
| ---------------- | ---------------------------------------------- |
| organizations    | Many roles belong to one organization (tenant) |
| role_permissions | One-to-many                                    |
| user_roles       | One-to-many                                    |

---

# 6. Columns

| Column      | Type         | Required | Notes                                             |
| ----------- | ------------ | -------- | ------------------------------------------------- |
| id          | ULID         | Yes      | Primary Key                                       |
| tenant_id   | ULID         | Yes      | Organization ownership                            |
| role_code   | VARCHAR(100) | Yes      | Stable unique identifier (e.g. `ORG_ADMIN`)       |
| role_name   | VARCHAR(150) | Yes      | Human-readable name                               |
| description | TEXT         | No       | Business description                              |
| role_type   | ENUM         | Yes      | `System` or `Organization`                        |
| is_default  | BOOLEAN      | Yes      | Assigned automatically to new users if applicable |
| is_system   | BOOLEAN      | Yes      | Protected platform role                           |
| created_at  | TIMESTAMPTZ  | Yes      | UTC                                               |
| created_by  | ULID         | No       | User who created the role                         |
| updated_at  | TIMESTAMPTZ  | Yes      | UTC                                               |
| updated_by  | ULID         | No       | User who last updated the role                    |
| deleted_at  | TIMESTAMPTZ  | No       | Soft delete timestamp                             |
| deleted_by  | ULID         | No       | User who performed the soft delete                |
| version     | INTEGER      | Yes      | Optimistic locking                                |

---

# 7. Validation Rules

* `role_code` must be uppercase with underscores (e.g. `HR_MANAGER`).
* `role_code` must be unique within the tenant.
* `role_name` is required.
* System roles cannot be renamed or deleted.
* Default roles must remain active.

---

# 8. Business Rules

* Every role belongs to exactly one tenant.
* Users may have multiple roles.
* Roles may contain multiple permissions.
* A role without permissions grants no access.
* Organization administrators may create organization roles.
* Only platform administrators may manage system roles.

---

# 9. Constraints

| Constraint  | Description                    |
| ----------- | ------------------------------ |
| Primary Key | `id`                           |
| Foreign Key | `tenant_id → organizations.id` |
| Unique      | `(tenant_id, role_code)`       |
| Check       | `role_name <> ''`              |

---

# 10. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Unique (`tenant_id`, `role_code`)
* Index (`role_name`)
* Index (`role_type`)
* Index (`is_default`)
* Index (`deleted_at`)

---

# 11. Security Classification

| Column      | Classification |
| ----------- | -------------- |
| role_code   | Internal       |
| role_name   | Internal       |
| description | Internal       |
| role_type   | Internal       |

Role definitions are configuration data but should only be editable by authorized administrators.

---

# 12. API Usage

Typical operations include:

* Create role
* Update role
* Archive role
* Assign permissions
* List available roles
* Set default role

Authorization for these operations must be enforced through the Identity Domain.

---

# 13. UI Usage

Primary screens:

* Role Management
* Security Administration
* Organization Settings
* User Assignment

The interface should display the role name and description while hiding internal identifiers from most users.

---

# 14. Example Record (Conceptual)

| Field       | Example                                      |
| ----------- | -------------------------------------------- |
| id          | 01JXKD2P4M8N6Q7R1S5T9U3V0W                   |
| tenant_id   | 01JXK9A8D7F5H3M2P8Q1R6S4T9                   |
| role_code   | HR_MANAGER                                   |
| role_name   | HR Manager                                   |
| description | Manages employee records and leave approvals |
| role_type   | Organization                                 |
| is_default  | false                                        |
| is_system   | false                                        |

---

# 15. Default System Roles

The platform should provide a baseline set of protected roles:

* Platform Administrator
* Organization Owner
* Organization Administrator
* Standard User
* Read-Only User

Organizations may add additional roles to meet their operational needs.

---

# 16. Future Enhancements

Future versions may support:

* Role inheritance
* Temporary role assignments
* Approval-based role activation
* Role expiration dates
* Context-aware roles
* Delegated administration

These features should extend the existing RBAC model without breaking backward compatibility.

---

# 17. Acceptance Criteria

The `roles` entity is complete when:

* Tenant-specific roles are supported.
* System and organization roles are distinguished.
* Relationships to permissions and user assignments are documented.
* Validation rules and constraints are defined.
* Security considerations are documented.
* API and UI dependencies are identified.

---

# Summary

The `roles` entity provides the organizational structure for authorization within Quantum Workforce OS. By grouping permissions into reusable business responsibilities, it enables flexible, secure, and scalable access control while allowing each tenant to tailor roles to its own operational needs.
