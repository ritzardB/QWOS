-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 002_users.sql
-- Version     : 1.0
-- Description : Users Table
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- USERS
--
-- Represents every authenticated identity within Quantum Workforce OS.
--
-- This table contains ONLY authentication and security information.
--
-- Personal profile information is stored in:
--
--     user_profiles
--
-- =============================================================================

CREATE TABLE users (

    -- -------------------------------------------------------------------------
    -- Primary Key
    -- -------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    -- -------------------------------------------------------------------------
    -- Tenant Ownership
    -- -------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    -- -------------------------------------------------------------------------
    -- Identity
    -- -------------------------------------------------------------------------

    email email_address NOT NULL,

    password_hash TEXT,

    account_status account_status
        NOT NULL
        DEFAULT 'PENDING',

    -- -------------------------------------------------------------------------
    -- Authentication
    -- -------------------------------------------------------------------------

    email_verified_at TIMESTAMPTZ,

    last_login_at TIMESTAMPTZ,

    password_changed_at TIMESTAMPTZ,

    failed_login_attempts INTEGER
        NOT NULL
        DEFAULT 0
        CHECK (failed_login_attempts >= 0),

    authentication_provider authentication_provider
        NOT NULL
        DEFAULT 'LOCAL',

    user_type user_type
        NOT NULL
        DEFAULT 'EMPLOYEE',

    -- -------------------------------------------------------------------------
    -- Audit
    -- -------------------------------------------------------------------------

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

    -- -------------------------------------------------------------------------
    -- Concurrency
    -- -------------------------------------------------------------------------

    version INTEGER
        NOT NULL
        DEFAULT 1,

    -- -------------------------------------------------------------------------
    -- Constraints
    -- -------------------------------------------------------------------------

    CONSTRAINT uq_users_email
        UNIQUE (tenant_id, email)

);

COMMIT;