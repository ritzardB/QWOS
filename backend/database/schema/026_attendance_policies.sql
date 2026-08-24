-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 026_attendance_policies.sql
-- Version     : 1.0
-- Description : Attendance policy definitions
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- ATTENDANCE POLICIES
-- =============================================================================

CREATE TABLE attendance_policies (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Policy Identity
    ---------------------------------------------------------------------------

    policy_code VARCHAR(50) NOT NULL,

    policy_name VARCHAR(150) NOT NULL,

    ---------------------------------------------------------------------------
    -- Attendance Requirement
    --
    -- Supported values:
    --
    --     not_required
    --     tracking_only
    --     required
    --
    ---------------------------------------------------------------------------

    attendance_requirement identifier_code
        NOT NULL
        DEFAULT 'required',

    ---------------------------------------------------------------------------
    -- Clocking Requirements
    ---------------------------------------------------------------------------

    clock_in_required BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    clock_out_required BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Payroll Impact
    ---------------------------------------------------------------------------

    payroll_impact_enabled BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    overtime_enabled BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    undertime_enabled BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    late_deduction_enabled BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    ---------------------------------------------------------------------------
    -- Attendance Tolerance
    ---------------------------------------------------------------------------

    grace_period_minutes INTEGER
        NOT NULL
        DEFAULT 0,

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

    CONSTRAINT uq_attendance_policies_code
        UNIQUE (
            tenant_id,
            policy_code
        ),

    CONSTRAINT chk_attendance_policies_code
        CHECK (
            LENGTH(TRIM(policy_code)) > 0
        ),

    CONSTRAINT chk_attendance_policies_name
        CHECK (
            LENGTH(TRIM(policy_name)) > 0
        ),

    CONSTRAINT chk_attendance_policies_grace_period
        CHECK (
            grace_period_minutes >= 0
        ),

    CONSTRAINT chk_attendance_policies_clocking
        CHECK (
            attendance_requirement = 'not_required'
            OR (
                clock_in_required
                OR clock_out_required
            )
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_attendance_policies_active
    ON attendance_policies(is_active);

CREATE INDEX idx_attendance_policies_tenant
    ON attendance_policies(tenant_id);

CREATE INDEX idx_attendance_policies_requirement
    ON attendance_policies(attendance_requirement);

COMMIT;