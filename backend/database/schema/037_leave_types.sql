-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 037_leave_types.sql
-- Version     : 1.0
-- Description : Tenant-defined leave type master definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the reusable leave categories available within a tenant.
--
-- Leave Type represents WHAT kind of leave exists.
--
-- Examples:
--
--   annual_leave
--   sick_leave
--   emergency_leave
--   maternity_leave
--   paternity_leave
--   unpaid_leave
--
-- Leave entitlement, accrual, carry-forward, eligibility, and approval rules
-- are intentionally handled by subsequent Leave Policy schemas.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE TYPES
-- =============================================================================

CREATE TABLE leave_types (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Identity
    ---------------------------------------------------------------------------

    leave_code identifier_code NOT NULL,

    leave_name VARCHAR(150) NOT NULL,

    description description_text,

    ---------------------------------------------------------------------------
    -- Compensation Classification
    ---------------------------------------------------------------------------

    is_paid BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

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

    CONSTRAINT chk_leave_types_name
        CHECK (
            LENGTH(TRIM(leave_name)) > 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_types_tenant
    ON leave_types(tenant_id);

CREATE INDEX idx_leave_types_active
    ON leave_types(is_active);

CREATE INDEX idx_leave_types_code
    ON leave_types(leave_code);

-- =============================================================================
-- UNIQUENESS
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_types_code
    ON leave_types(
        tenant_id,
        leave_code
    )
    WHERE deleted_at IS NULL;

COMMIT;