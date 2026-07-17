-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 014_security_policies.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Description : Organization Security Policies
-- =============================================================================

BEGIN;

CREATE TABLE security_policies (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Organization
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Password Policy
    ---------------------------------------------------------------------------

    minimum_password_length INTEGER
        NOT NULL
        DEFAULT 12,

    password_expiry_days INTEGER
        NOT NULL
        DEFAULT 90,

    password_history INTEGER
        NOT NULL
        DEFAULT 5,

    ---------------------------------------------------------------------------
    -- Authentication
    ---------------------------------------------------------------------------

    max_failed_login_attempts INTEGER
        NOT NULL
        DEFAULT 5,

    account_lockout_minutes INTEGER
        NOT NULL
        DEFAULT 30,

    require_mfa BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    allow_concurrent_sessions BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    session_timeout_minutes INTEGER
        NOT NULL
        DEFAULT 1440,

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

    version INTEGER
        NOT NULL
        DEFAULT 1

);

COMMIT;