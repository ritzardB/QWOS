-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 007_user_roles.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--      004_roles.sql
--
-- Description : User Role Assignments
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- USER ROLES
--
-- Represents a business entity assigning a role to a user.
--
-- =============================================================================

CREATE TABLE user_roles (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Assignment
    ---------------------------------------------------------------------------

    user_id ulid NOT NULL,

    role_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Assignment Lifecycle
    ---------------------------------------------------------------------------

    is_primary BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    is_enabled BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    assigned_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    assigned_by ulid,

    effective_from TIMESTAMPTZ,

    effective_until TIMESTAMPTZ,

    assignment_reason description_text,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    created_by ulid,

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    updated_by ulid,

    deleted_at TIMESTAMPTZ,

    deleted_by ulid,

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER
        NOT NULL
        DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_user_roles
        UNIQUE (
            tenant_id,
            user_id,
            role_id
        ),

    CONSTRAINT chk_user_roles_dates
        CHECK (
            effective_until IS NULL
            OR effective_from IS NULL
            OR effective_until > effective_from
        )

);

COMMIT;
