-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 009_session_tokens.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Depends On  :
--      000_extensions.sql
--      001_enums.sql
--      001a_domains.sql
--      002_users.sql
--      008_sessions.sql
--
-- Description : Session Refresh Tokens
--
-- =============================================================================

BEGIN;

CREATE TABLE session_tokens (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Parent Session
    ---------------------------------------------------------------------------

    session_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Token
    ---------------------------------------------------------------------------

    token_hash TEXT NOT NULL,

    token_type identifier_code
        NOT NULL
        DEFAULT 'REFRESH',

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    issued_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expires_at TIMESTAMPTZ
        NOT NULL,

    last_used_at TIMESTAMPTZ,

    revoked_at TIMESTAMPTZ,

    revoked_by ulid,

    revocation_reason description_text,

    ---------------------------------------------------------------------------
    -- Rotation
    ---------------------------------------------------------------------------

    rotated_from_token_id ulid,

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

    CONSTRAINT fk_session_tokens_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_session_tokens_rotated
        FOREIGN KEY (rotated_from_token_id)
        REFERENCES session_tokens(id),

    CONSTRAINT uq_session_token_hash
        UNIQUE (token_hash),

    CONSTRAINT chk_session_token_expiry
        CHECK (expires_at > issued_at)

);

CREATE INDEX idx_session_tokens_session
    ON session_tokens(session_id);

CREATE INDEX idx_session_tokens_expires
    ON session_tokens(expires_at);

COMMIT;