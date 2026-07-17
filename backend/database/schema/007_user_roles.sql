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
-- Assigns one or more roles to authenticated users.
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
    -- Assignment Properties
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

    effective_from TIMESTAMPTZ,-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 006_user_roles.sql
-- Version     : 1.0
-- Description : User Role Assignments
--
-- =============================================================================

BEGIN;

CREATE TABLE user_roles (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Relationships
    ---------------------------------------------------------------------------

    user_id CHAR(26)
        NOT NULL,

    role_id CHAR(26)
        NOT NULL,

    ---------------------------------------------------------------------------
    -- Assignment
    ---------------------------------------------------------------------------

    assigned_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    assigned_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    created_by CHAR(26),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    updated_by CHAR(26),

    deleted_at TIMESTAMPTZ,

    deleted_by CHAR(26),

    version INTEGER
        NOT NULL
        DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT uq_user_roles
        UNIQUE (tenant_id, user_id, role_id),

    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE

);

COMMIT;