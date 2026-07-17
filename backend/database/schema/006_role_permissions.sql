-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 006_role_permissions.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--      004_roles.sql
--      005_permissions.sql
--
-- Description : Role Permission Assignments
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- ROLE PERMISSIONS
--
-- Associates permissions with roles.
--
-- This is a business entity, not merely a junction table.
--
-- =============================================================================

CREATE TABLE role_permissions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Assignment
    ---------------------------------------------------------------------------

    role_id CHAR(26) NOT NULL,

    permission_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Assignment Lifecycle
    ---------------------------------------------------------------------------

    is_enabled BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    granted_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    granted_by CHAR(26),

    effective_from TIMESTAMPTZ,

    effective_until TIMESTAMPTZ,

    assignment_reason description_text,

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

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER
        NOT NULL
        DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT fk_role_permissions_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id),

    CONSTRAINT fk_role_permissions_permission
        FOREIGN KEY (permission_id)
        REFERENCES permissions(id),

    CONSTRAINT uq_role_permission
        UNIQUE (
            tenant_id,
            role_id,
            permission_id
        ),

    CONSTRAINT chk_role_permission_dates
        CHECK (
            effective_until IS NULL
            OR effective_from IS NULL
            OR effective_until > effective_from
        )

);

COMMIT;