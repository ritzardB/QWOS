-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 013_invitations.sql
-- Version     : 1.0.0
-- Status      : Production
-- Owner       : Database Architecture Team
-- Description : Organization Invitations
-- =============================================================================

BEGIN;

CREATE TABLE invitations (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id ulid PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Organization
    ---------------------------------------------------------------------------

    tenant_id ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Invitation
    ---------------------------------------------------------------------------

    invited_email email_address NOT NULL,

    invitation_token_hash token_hash NOT NULL,

    role_id ulid,

    invited_by ulid NOT NULL,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    requested_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expires_at TIMESTAMPTZ
        NOT NULL,

    accepted_at TIMESTAMPTZ,

    revoked_at TIMESTAMPTZ,

    status invitation_status
        NOT NULL
        DEFAULT 'PENDING',

    ---------------------------------------------------------------------------
    -- Client Information
    ---------------------------------------------------------------------------

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

    CONSTRAINT fk_invitations_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id),

    CONSTRAINT fk_invitations_invited_by
        FOREIGN KEY (invited_by)
        REFERENCES users(id),

    CONSTRAINT chk_invitation_expiry
        CHECK (
            expires_at > requested_at
        )

);

COMMIT;