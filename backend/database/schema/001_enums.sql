-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 001_enums.sql
-- Version     : 1.0
-- Description : Shared Enumerated Types
--
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- Authentication Provider
-- -----------------------------------------------------------------------------

CREATE TYPE authentication_provider AS ENUM (
    'LOCAL',
    'GOOGLE',
    'MICROSOFT',
    'APPLE',
    'GITHUB',
    'SAML'
);

-- -----------------------------------------------------------------------------
-- User Type
-- -----------------------------------------------------------------------------

CREATE TYPE user_type AS ENUM (
    'SYSTEM',
    'EMPLOYEE',
    'CONTRACTOR',
    'CUSTOMER',
    'VENDOR'
);

-- -----------------------------------------------------------------------------
-- Account Status
-- -----------------------------------------------------------------------------

CREATE TYPE account_status AS ENUM (
    'PENDING',
    'ACTIVE',
    'LOCKED',
    'SUSPENDED',
    'DISABLED'
);

-- -----------------------------------------------------------------------------
-- Role Type
-- -----------------------------------------------------------------------------

CREATE TYPE role_type AS ENUM (
    'SYSTEM',
    'ORGANIZATION'
);

-- -----------------------------------------------------------------------------
-- Permission Category
-- -----------------------------------------------------------------------------

CREATE TYPE permission_category AS ENUM (
    'CRUD',
    'WORKFLOW',
    'REPORTING',
    'ADMINISTRATION',
    'INTEGRATION'
);

-- -----------------------------------------------------------------------------
-- Login Result
-- -----------------------------------------------------------------------------

CREATE TYPE login_result AS ENUM (
    'SUCCESS',
    'INVALID_CREDENTIALS',
    'ACCOUNT_LOCKED',
    'ACCOUNT_DISABLED',
    'PASSWORD_EXPIRED',
    'MFA_REQUIRED',
    'MFA_FAILED',
    'RATE_LIMITED'
);

-- -----------------------------------------------------------------------------
-- Password Reset Status
-- -----------------------------------------------------------------------------

CREATE TYPE password_reset_status AS ENUM (
    'PENDING',
    'USED',
    'EXPIRED',
    'REVOKED'
);

-- -----------------------------------------------------------------------------
-- Email Verification Status
-- -----------------------------------------------------------------------------

CREATE TYPE email_verification_status AS ENUM (
    'PENDING',
    'VERIFIED',
    'EXPIRED',
    'REVOKED'
);

-- -----------------------------------------------------------------------------
-- Invitation Status
-- -----------------------------------------------------------------------------

CREATE TYPE invitation_status AS ENUM (
    'PENDING',
    'ACCEPTED',
    'EXPIRED',
    'REVOKED'
);

COMMIT;