-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 012_email_verifications.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--
-- Description : Email Verification Requests
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMAIL VERIFICATIONS
--
-- Stores email verification requests.
--
-- Verification tokens are stored only as cryptographic hashes.
--
-- =============================================================================

CREATE TABLE email_verifications (

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
    -- Email
    ---------------------------------------------------------------------------

    email email_address NOT NULL,

    verification_token_hash token_hash
        NOT NULL,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    requested_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expires_at TIMESTAMPTZ
        NOT NULL,

    verified_at TIMESTAMPTZ,

    revoked_at TIMESTAMPTZ,

    status email_verification_status
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

    CONSTRAINT fk_email_verifications_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT chk_email_verification_expiry
        CHECK (
            expires_at > requested_at
        ),

    CONSTRAINT chk_email_verification_verified
        CHECK (
            verified_at IS NULL
            OR verified_at >= requested_at
        )

);

COMMIT;