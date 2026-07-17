-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 010_login_history.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      002_users.sql
--      008_sessions.sql
--
-- Description : Login History
--
-- =============================================================================

BEGIN;

CREATE TABLE login_history (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- User / Session
    ---------------------------------------------------------------------------

    user_id ulid,

    session_id ulid,

    ---------------------------------------------------------------------------
    -- Authentication
    ---------------------------------------------------------------------------

    login_method identifier_code
        NOT NULL,

    authentication_result identifier_code
        NOT NULL,

    failure_reason description_text,

    ---------------------------------------------------------------------------
    -- Client
    ---------------------------------------------------------------------------

    ip_address ip_address,

    device_name VARCHAR(150),

    browser_name VARCHAR(100),

    operating_system VARCHAR(100),

    user_agent TEXT,

    ---------------------------------------------------------------------------
    -- Event
    ---------------------------------------------------------------------------

    occurred_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

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

    CONSTRAINT fk_login_history_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_login_history_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(id)
        ON DELETE SET NULL

);

CREATE INDEX idx_login_history_user
    ON login_history(user_id);

CREATE INDEX idx_login_history_time
    ON login_history(occurred_at);

CREATE INDEX idx_login_history_result
    ON login_history(authentication_result);

COMMIT;