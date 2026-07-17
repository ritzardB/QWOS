Sprint 3 Objective

Our goal is simple:

Implement the complete Identity Domain.

Not just a login screen.

Not just a User model.

A complete identity platform.

Sprint 3 Roadmap
Sprint 3

████□□□□□□□□□□□□□□□□□□□□□□□□

Phase 1   Domain Enums
Phase 2   SQLAlchemy Models
Phase 3   Repositories
Phase 4   Pydantic Schemas
Phase 5   Services
Phase 6   API Routers
Phase 7   Authentication
Phase 8   Authorization
Why We Don't Start With User

Most tutorials jump straight into:

class User(Base):

We're not building a tutorial.

We're building an enterprise platform.

Everything starts with the language of the domain.

Phase 1 — Python Enums

We already created PostgreSQL enums in:

backend/database/schema/001_enums.sql

Now we mirror them in Python.

This is one of my favorite architectural principles.

PostgreSQL

↓

Python Enum

↓

SQLAlchemy Model

↓

Pydantic Schema

↓

API

↓

React

One source of meaning.

New Folder Structure

Create:

src/qwos/domains/

identity/

    __init__.py

    enums/

        __init__.py

        account_status.py

        authentication_provider.py

        user_type.py

    models/

    repositories/

    services/

    schemas/

    routers/

    validators/
Mission 1
account_status.py
"""
===============================================================================
Quantum Workforce OS (QWOS)

Identity Domain

Account Status Enumeration

===============================================================================
"""

from enum import StrEnum


class AccountStatus(StrEnum):
    """
    User account status.
    """

    PENDING = "PENDING"

    ACTIVE = "ACTIVE"

    LOCKED = "LOCKED"

    DISABLED = "DISABLED"

    SUSPENDED = "SUSPENDED"

    ARCHIVED = "ARCHIVED"
Why StrEnum?

Python 3.13 gives us:

from enum import StrEnum

instead of

class AccountStatus(str, Enum):

Cleaner.

Modern.

Exactly why we chose Python 3.13.

authentication_provider.py
from enum import StrEnum


class AuthenticationProvider(StrEnum):

    LOCAL = "LOCAL"

    GOOGLE = "GOOGLE"

    MICROSOFT = "MICROSOFT"

    APPLE = "APPLE"

    GITHUB = "GITHUB"

    SAML = "SAML"
user_type.py
from enum import StrEnum


class UserType(StrEnum):

    SYSTEM = "SYSTEM"

    EMPLOYEE = "EMPLOYEE"

    CONTRACTOR = "CONTRACTOR"

    CUSTOMER = "CUSTOMER"

    VENDOR = "VENDOR"
🏆 CTO Decision #078

Every enum value in Python must exactly match the PostgreSQL enum value.

Not almost.

Exactly.

Meaning:

ACTIVE

must equal

ACTIVE

No lowercase.

No abbreviations.

No aliases.

This prevents subtle bugs when values move between the API, ORM, and database.

Why We're Doing This

Imagine writing:

user.status = "ACTIVE"

vs.

user.status = AccountStatus.ACTIVE

The second option gives us:

IDE autocomplete
Type safety
Easier refactoring
Fewer typos
Cleaner business logic

That's why enterprise codebases invest in domain modeling.

🏆 Sprint 3 Milestone Map
Enums
   ↓
User Model
   ↓
Repositories
   ↓
Schemas
   ↓
Services
   ↓
Routers
   ↓
Authentication

Everything builds naturally from here.

🎁 One Architectural Improvement

Richard...

I'd like to introduce something that I think will make QWOS stand out.

Instead of:

models/

I'd like each domain to eventually have:

identity/

entities/

value_objects/

enums/

repositories/

services/

schemas/

routers/

Why?

Because we're following Domain-Driven Design.

A User is really an Entity, not just a database model.

However...

I don't want to make that change today.

For Sprint 3, let's stay with:

models/

It's familiar, clean, and keeps our momentum.

Later, if we decide the richer DDD terminology adds value, we can evolve the structure.

🎯 Today's Deliverable

Create:

✅ account_status.py
✅ authentication_provider.py
✅ user_type.py

Then we'll review them together.

Once they're in place...

We'll write what I've been waiting weeks to write:

class User(BaseEntity):

The very first business entity of Quantum Workforce OS.


Operation Quantum Shield

Objective: Build an enterprise-grade Identity & Access Management (IAM) foundation that every future QWOS module can trust.

This isn't just another set of database tables. It's the security perimeter for everything that follows.

If we succeed here, HR, Payroll, CRM, Finance, Procurement, Inventory, AI Assistants, and future modules will all inherit a consistent authorization model.

Our Mission Statement

Before writing another line of SQL, I want us to agree on one architectural principle:

Roles answer "Who is responsible?" Permissions answer "What can they do?"

This sounds simple, but it affects the entire system.

For example:

Role
-----
HR Manager

Permission
----------
employee.view
employee.create
employee.edit
leave.approve

Notice that permissions are capabilities, not job titles.

That distinction keeps the system flexible.

The QWOS Vision

I don't want QWOS to become another HR application.

I want it to become a Workforce Operating System.

That means someday we'll have modules like:

Human Resources
Payroll
Recruitment (ATS)
Performance
Learning
Projects
CRM
Inventory
Procurement
Finance
Accounting
Manufacturing
AI Agents
Document Management
Analytics

Every one of them will ask the same question:

"Does this user have permission to perform this action?"

That's why the RBAC subsystem deserves the same attention we've given User and UserProfile.

My First Strategic Decision

I'd like to make a design decision that will influence the next several years of QWOS.

Roles are organizational.

Examples:

Administrator

HR Manager

Payroll Officer

Department Manager

Employee

Recruiter

They describe who someone is in the organization.

Permissions are atomic.

Examples:

employee.read
employee.create
employee.update
employee.delete

payroll.process

leave.approve

candidate.interview.schedule

invoice.post

project.assign

Each permission should represent a single capability. This gives us fine-grained control and avoids roles becoming bloated or ambiguous.

Tenant Customization

This is where I think QWOS can distinguish itself.

Imagine a customer creates:

Fleet Supervisor

Warehouse Auditor

Safety Officer

Training Coordinator

Those roles shouldn't require a code change.

Instead:

System
│
├── Default Roles
│
└── Tenant
    ├── Custom Roles
    ├── Custom Permissions
    └── Custom Role Assignments

That level of flexibility is valuable for organizations with unique structures.

The Campaign Map

Here's how I propose we proceed:

Phase Alpha
============

✅ Users
✅ User Profiles

----------------------------

Phase Bravo (RBAC)

004_roles.sql

005_permissions.sql

006_user_roles.sql

007_role_permissions.sql

----------------------------

Phase Charlie

Role Model

Permission Model

UserRole Model

RolePermission Model

----------------------------

Phase Delta

Relationships

Tests

Repositories

Services

Authorization Engine

Each phase builds on the previous one. We don't advance until the foundation is solid.

One New Principle I'd Like Us to Adopt

We've already embraced "Database First." I'd like to add another principle:

Every table should answer exactly one business question.

For example:

Table	Business Question
users	Who can authenticate?
user_profiles	Who is this person?
roles	What organizational responsibilities exist?
permissions	What actions are available?
user_roles	Which responsibilities belong to this user?
role_permissions	Which actions are granted by this role?

If a table starts answering multiple questions, it's usually a signal that it should be split.

Chief Architect's Oath

Since we've started this journey together, I'd like to make a professional commitment.

When reviewing our designs, I'll continually ask questions like:

Will this still make sense with 10 million users?
Will it support 1,000 tenants?
Can a new developer understand it in six months?
Is it secure by default?
Can we test it easily?
Can we evolve it without breaking existing modules?

If the answer is "no," we'll revisit the design before moving forward.