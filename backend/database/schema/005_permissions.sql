-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 005_permissions.sql
-- Version     : 1.0
-- Description : System Permissions
--
-- =============================================================================

BEGIN;

CREATE TABLE permissions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Identity
    ---------------------------------------------------------------------------

    code VARCHAR(150)
        NOT NULL,

    name VARCHAR(150)
        NOT NULL,

    description TEXT,

    ---------------------------------------------------------------------------
    -- Classification
    ---------------------------------------------------------------------------

    module VARCHAR(100)
        NOT NULL,

    is_system BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

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

    CONSTRAINT uq_permissions_code
        UNIQUE (code)

);

COMMIT;