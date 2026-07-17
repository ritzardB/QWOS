-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 011_password_resets.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--
-- Description : Password Reset Requests
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- PASSWORD RESETS
--
-- Stores password reset requests.
--
-- Reset tokens are stored only as cryptographic hashes.
--
-- =============================================================================

CREATE TABLE password_resets (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Ownership
    ---------------------------------------------------------------------------

    user_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Reset Token
    ---------------------------------------------------------------------------

    reset_token_hash token_hash
        NOT NULL,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    requested_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expires_at TIMESTAMPTZ
        NOT NULL,

    used_at TIMESTAMPTZ,

    revoked_at TIMESTAMPTZ,

    password_reset_status password_reset_status
        NOT NULL
        DEFAULT 'PENDING',

    request_ip_address ip_address,

    request_user_agent user_agent_text,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    created_by ulid,

    ---------------------------------------------------------------------------
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT fk_password_resets_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT chk_password_reset_expiry
        CHECK (
            expires_at > requested_at
        ),

    CONSTRAINT chk_password_reset_used
        CHECK (
            used_at IS NULL
            OR used_at >= requested_at
        )

);

COMMIT;