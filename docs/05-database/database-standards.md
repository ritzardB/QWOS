# Quantum Workforce OS (QWOS)

# Database Standards

**Document ID:** DB-000

**Standard Name:** Quantum Database Standard (QDS)

**Version:** 1.0

**Status:** Draft

**Author:** Richard Balabarcon / Quantum Virtual Solutions

**Date:** July 2026

---

# 1. Purpose

The Quantum Database Standard (QDS) defines the mandatory conventions, naming standards, design principles, and governance rules for all database objects within Quantum Workforce OS.

Its objectives are to:

* Ensure consistency across all domains.
* Improve maintainability.
* Support multi-tenancy.
* Simplify development.
* Strengthen security.
* Improve performance.
* Enable future scalability.

These standards apply to every table, view, index, constraint, migration, and database object.

---

# 2. Database Philosophy

The database is a core business asset.

It is not merely a storage mechanism.

Every table represents a business concept.

Every relationship reflects a business rule.

Every column has a defined purpose.

The database should remain understandable without requiring knowledge of application code.

---

# 3. General Principles

The database shall be:

* Normalized (Third Normal Form unless justified otherwise)
* Multi-tenant aware
* Audit-friendly
* Secure by default
* Backward compatible where practical
* Optimized for readability before optimization
* Documented before implementation

---

# 4. Primary Key Standard

All primary keys shall use **ULID**.

Example:

```text
01JXK9Y8T8K5K6WQ2E7M4J1S9A
```

Reasons:

* Globally unique
* Lexicographically sortable
* Distributed-system friendly
* Better index locality than random UUIDs

Primary key column name:

```text
id
```

---

# 5. Table Naming

Tables use:

* lowercase
* plural nouns
* snake_case

Examples:

```text
users
roles
permissions
projects
tasks
employees
```

Avoid:

```text
tbl_users
User
EmployeeMaster
```

---

# 6. Column Naming

Columns use:

* snake_case
* descriptive names
* singular form where appropriate

Examples:

```text
first_name
last_name
email
created_at
organization_id
```

Avoid abbreviations unless universally understood.

---

# 7. Foreign Key Standard

Foreign keys follow:

```text
<referenced_table_singular>_id
```

Examples:

```text
organization_id
user_id
project_id
client_id
role_id
```

---

# 8. Mandatory Audit Columns

Every business table shall contain:

| Column     | Purpose                           |
| ---------- | --------------------------------- |
| id         | Primary Key (ULID)                |
| tenant_id  | Tenant ownership                  |
| created_at | Record creation timestamp         |
| created_by | User who created the record       |
| updated_at | Last modification timestamp       |
| updated_by | User who last modified the record |
| deleted_at | Soft delete timestamp             |
| deleted_by | User who performed soft delete    |
| version    | Optimistic locking version        |

These fields provide traceability, concurrency control, and support for multi-tenancy.

---

# 9. Timestamp Standard

All timestamps:

* Stored in UTC.
* Use timezone-aware data types.
* Named with the `_at` suffix.

Examples:

```text
created_at
updated_at
deleted_at
last_login_at
verified_at
```

---

# 10. Soft Delete Policy

Business records are never physically deleted.

Instead:

* Active record → `deleted_at IS NULL`
* Deleted record → `deleted_at` contains a timestamp

Hard deletes are reserved for exceptional maintenance scenarios and must be documented.

---

# 11. Boolean Naming

Boolean columns begin with:

* `is_`
* `has_`
* `can_`

Examples:

```text
is_active
is_verified
has_avatar
can_login
```

---

# 12. Enum Strategy

Use enums only for values that are stable and unlikely to change frequently.

Examples:

* User status
* Authentication provider
* Gender (if applicable)

Use lookup/reference tables for business-configurable values such as leave types or project priorities.

---

# 13. Constraints

Every table should include appropriate constraints:

* Primary Key
* Foreign Key
* Unique
* Check Constraints
* NOT NULL where required

Database constraints complement application validation—they do not replace it.

---

# 14. Indexing Strategy

Create indexes based on query patterns, not assumptions.

Common indexes include:

* Primary Key
* Foreign Keys
* Email
* Tenant ID
* Frequently searched columns

Composite indexes should be added only after confirming the access patterns.

---

# 15. Tenant Isolation

Every business record belongs to exactly one tenant.

Requirements:

* `tenant_id` is mandatory.
* Queries must be tenant-scoped.
* Cross-tenant access is prohibited unless explicitly authorized for platform administration.

---

# 16. Data Classification

Each column should be classified to guide access control and protection.

| Classification | Examples                     |
| -------------- | ---------------------------- |
| Public         | Company name                 |
| Internal       | Department                   |
| Confidential   | Salary                       |
| Restricted     | Password hash, refresh token |

Restricted data requires additional protection and access controls.

---

# 17. Security Standards

Sensitive data must never be stored in plain text.

Examples:

* Passwords → hashed
* Refresh tokens → hashed where practical
* Secrets → encrypted
* Personally identifiable information (PII) protected according to policy

Security controls should be reviewed regularly.

---

# 18. Migration Standards

All schema changes must be implemented through version-controlled migrations.

Guidelines:

* One logical change per migration.
* Migrations are reviewed before execution.
* Rollback strategy documented when feasible.
* Production data migrations tested in non-production environments first.

---

# 19. Backup and Recovery

Database operations must support:

* Automated backups
* Point-in-time recovery (where supported)
* Periodic restore testing
* Documented recovery procedures

Recovery objectives (RPO/RTO) should be defined for production deployments.

---

# 20. Performance Guidelines

Performance improvements should be driven by evidence.

Priorities:

1. Correct data model
2. Efficient queries
3. Appropriate indexes
4. Caching when justified
5. Denormalization only when supported by measurable performance needs

---

# 21. Example Base Entity

Conceptually, every business table includes:

```text
id
tenant_id
created_at
created_by
updated_at
updated_by
deleted_at
deleted_by
version
```

Application models should inherit these common fields where appropriate to ensure consistency.

---

# 22. Governance

Database changes require:

* Business requirement
* Architecture review
* Updated documentation
* Migration
* Testing
* Approval before release

No direct production schema changes are permitted outside the defined deployment process.

---

# 23. Compliance Checklist

Before introducing a new table, confirm:

* [ ] Business purpose documented
* [ ] Domain ownership defined
* [ ] Naming follows QDS
* [ ] Audit columns included
* [ ] Tenant support implemented
* [ ] Appropriate indexes identified
* [ ] Security classification assigned
* [ ] Migration prepared
* [ ] Documentation updated

---

# Summary

The Quantum Database Standard establishes the foundation for every database object within Quantum Workforce OS.

By applying consistent naming, governance, security, and design principles, QWOS maintains a database that is scalable, secure, maintainable, and aligned with long-term product goals.

All future database design must comply with this standard unless an approved Architecture Decision Record (ADR) documents a justified exception.
