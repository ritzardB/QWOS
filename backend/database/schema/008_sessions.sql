-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 008_sessions.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--
-- Description : User Authentication Sessions
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- SESSIONS
--
-- Represents authenticated user sessions.
--
-- A user may have multiple concurrent sessions across multiple devices.
--
-- =============================================================================

CREATE TABLE sessions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Owner
    ---------------------------------------------------------------------------

    user_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Session
    ---------------------------------------------------------------------------

    session_name VARCHAR(100),

    device_name VARCHAR(150),

    browser_name VARCHAR(100),

    operating_system VARCHAR(100),

    ip_address ip_address,

    user_agent TEXT,

    ---------------------------------------------------------------------------
    -- Authentication
    ---------------------------------------------------------------------------

    signed_in_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    last_activity_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expires_at TIMESTAMPTZ NOT NULL,

    signed_out_at TIMESTAMPTZ,

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

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

    CONSTRAINT fk_sessions_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),
        ON DELETE CASCADE,

    CONSTRAINT chk_session_expiry
        CHECK (
            expires_at > signed_in_at
        )

);

COMMIT;