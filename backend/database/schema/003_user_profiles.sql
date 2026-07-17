-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 003_user_profiles.sql
-- Version     : 1.0
-- Description : User Profiles
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- USER PROFILES
--
-- Stores personal profile information.
--
-- Authentication information belongs to:
--
--     users
--
-- =============================================================================

CREATE TABLE user_profiles (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Identity
    ---------------------------------------------------------------------------

    user_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Personal Information
    ---------------------------------------------------------------------------

    first_name person_name NOT NULL,

    middle_name person_name,

    last_name person_name NOT NULL,

    display_name display_name NOT NULL,

    preferred_name person_name,

    ---------------------------------------------------------------------------
    -- Localization
    ---------------------------------------------------------------------------

    locale VARCHAR(10)
        NOT NULL
        DEFAULT 'en-US',

    language_code VARCHAR(10)
        DEFAULT 'en',

    timezone VARCHAR(100)
        NOT NULL
        DEFAULT 'UTC',

    ---------------------------------------------------------------------------
    -- Profile
    ---------------------------------------------------------------------------

    avatar_url TEXT,

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

    CONSTRAINT uq_user_profiles_user
        UNIQUE (user_id),

    CONSTRAINT fk_user_profiles_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

);

COMMIT;