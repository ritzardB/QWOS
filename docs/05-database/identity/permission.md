# Quantum Workforce OS (QWOS)

# Permissions Entity Specification

**Document ID:** DB-IDENTITY-005

**Entity:** Permissions

**Table:** `permissions`

**Domain:** Identity

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The `permissions` entity defines the smallest unit of authorization within Quantum Workforce OS.

A permission grants the ability to perform a specific action on a specific business resource.

Permissions are assigned to roles through the `role_permissions` relationship. Users receive permissions by being assigned one or more roles.

Permissions are never assigned directly to users in Version 1.0.

---

# 2. Business Responsibilities

The `permissions` entity is responsible for:

* Defining authorized actions.
* Supporting Role-Based Access Control (RBAC).
* Enabling consistent authorization across APIs and user interfaces.
* Providing a reusable authorization vocabulary for every business domain.

---

# 3. Table Name

```text
permissions
```

---

# 4. Owner

Identity Domain

---

# 5. Relationships

| Related Entity   | Relationship |
| ---------------- | ------------ |
| role_permissions | One-to-many  |

Permissions are intentionally independent of users. User access is determined through assigned roles.

---

# 6. Columns

| Column          | Type         | Required | Notes                                                  |
| --------------- | ------------ | -------- | ------------------------------------------------------ |
| id              | ULID         | Yes      | Primary Key                                            |
| permission_code | VARCHAR(150) | Yes      | Unique machine-readable identifier                     |
| permission_name | VARCHAR(150) | Yes      | Human-readable name                                    |
| description     | TEXT         | No       | Business description                                   |
| domain          | VARCHAR(50)  | Yes      | Owning business domain                                 |
| resource        | VARCHAR(50)  | Yes      | Protected resource                                     |
| action          | VARCHAR(50)  | Yes      | Authorized operation                                   |
| category        | ENUM         | Yes      | CRUD, Workflow, Reporting, Administration, Integration |
| is_system       | BOOLEAN      | Yes      | Platform-managed permission                            |
| created_at      | TIMESTAMPTZ  | Yes      | UTC                                                    |
| created_by      | ULID         | No       | User who created the permission                        |
| updated_at      | TIMESTAMPTZ  | Yes      | UTC                                                    |
| updated_by      | ULID         | No       | User who last updated the permission                   |
| deleted_at      | TIMESTAMPTZ  | No       | Soft delete timestamp                                  |
| deleted_by      | ULID         | No       | User who performed the soft delete                     |
| version         | INTEGER      | Yes      | Optimistic locking                                     |

---

# 7. Permission Naming Standard

Every permission follows the convention:

```text
<domain>.<resource>.<action>
```

Examples:

```text
identity.users.read
identity.users.create
identity.users.update
identity.users.delete

organization.departments.manage

crm.clients.read

crm.clients.create

work.projects.assign

work.tasks.complete

finance.payroll.approve

knowledge.documents.publish

platform.audit_logs.read
```

Permission codes are immutable once released.

---

# 8. Validation Rules

* `permission_code` must be unique across the platform.
* Codes use lowercase and dot notation.
* `domain`, `resource`, and `action` are required.
* `permission_name` is required.
* System permissions cannot be modified by tenant administrators.

---

# 9. Business Rules

* Every permission belongs to one business domain.
* Permissions represent a single action only.
* Permissions are assigned to roles—not directly to users.
* Platform upgrades may introduce new system permissions.
* Custom tenant permissions are reserved for future versions.

---

# 10. Constraints

| Constraint  | Description                       |
| ----------- | --------------------------------- |
| Primary Key | `id`                              |
| Unique      | `permission_code`                 |
| Check       | Required fields must not be empty |

---

# 11. Index Strategy

Recommended indexes:

* Primary Key (`id`)
* Unique (`permission_code`)
* Index (`domain`)
* Index (`resource`)
* Index (`action`)
* Index (`category`)
* Index (`deleted_at`)

---

# 12. Security Classification

| Column          | Classification |
| --------------- | -------------- |
| permission_code | Internal       |
| permission_name | Internal       |
| description     | Internal       |

Permission definitions are platform configuration data and should only be modified by authorized platform administrators.

---

# 13. API Usage

Typical operations include:

* List permissions
* View permission details
* Assign permissions to roles
* Search permissions by domain or category

Permission management APIs should be restricted to privileged administrative users.

---

# 14. UI Usage

Primary screens:

* Permission Catalog
* Role Management
* Security Administration

Permissions should be grouped by domain and category to improve usability.

---

# 15. Example Records

| Permission Code         | Name            |
| ----------------------- | --------------- |
| identity.users.read     | View Users      |
| identity.users.create   | Create Users    |
| crm.clients.update      | Update Clients  |
| work.tasks.assign       | Assign Tasks    |
| finance.payroll.approve | Approve Payroll |

---

# 16. Future Enhancements

Future versions may support:

* Conditional permissions
* Time-limited permissions
* Delegated permissions
* Dynamic policy evaluation
* Attribute-Based Access Control (ABAC)

These enhancements should build on the existing RBAC model without introducing breaking changes.

---

# 17. Acceptance Criteria

The `permissions` entity is complete when:

* Permission naming standards are documented.
* Domain ownership is defined.
* Relationships to roles are documented.
* Validation rules and constraints are specified.
* Security classifications are assigned.
* API and UI dependencies are identified.

---

# Summary

The `permissions` entity forms the foundation of authorization within Quantum Workforce OS. By defining clear, reusable, and domain-oriented permissions, the platform achieves consistent access control across business domains while remaining scalable and maintainable as new features are introduced.
