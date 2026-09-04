-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 038_leave_policies.sql
-- Version     : 1.0
-- Description : Leave entitlement and accrual policies
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines the rules governing how a leave type is administered within a
-- tenant.
--
-- Leave Type  = WHAT kind of leave exists
-- Leave Policy = HOW that leave is governed
--
-- Employee-specific assignment is handled separately by
-- 039_employee_leave_assignments.sql.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE POLICIES
-- =============================================================================

CREATE TABLE leave_policies (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Type
    ---------------------------------------------------------------------------

    leave_type_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Policy Identity
    ---------------------------------------------------------------------------

    policy_code identifier_code NOT NULL,

    policy_name VARCHAR(150) NOT NULL,

    description description_text,

    ---------------------------------------------------------------------------
    -- Entitlement
    ---------------------------------------------------------------------------

    entitlement_days NUMERIC(8,2)
        NOT NULL
        DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Accrual
    ---------------------------------------------------------------------------

    accrual_method identifier_code
        NOT NULL
        DEFAULT 'annual',

    accrual_frequency identifier_code
        NOT NULL
        DEFAULT 'monthly',

    ---------------------------------------------------------------------------
    -- Carry Forward
    ---------------------------------------------------------------------------

    carry_forward_allowed BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    carry_forward_days NUMERIC(8,2),

    ---------------------------------------------------------------------------
    -- Eligibility
    ---------------------------------------------------------------------------

    minimum_service_days INTEGER
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

    CONSTRAINT fk_leave_policies_leave_type
        FOREIGN KEY (leave_type_id)
        REFERENCES leave_types(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_policies_name
        CHECK (
            LENGTH(TRIM(policy_name)) > 0
        ),

    CONSTRAINT chk_leave_policies_entitlement
        CHECK (
            entitlement_days >= 0
        ),

    CONSTRAINT chk_leave_policies_carry_forward
        CHECK (
            carry_forward_days IS NULL
            OR carry_forward_days >= 0
        ),

    CONSTRAINT chk_leave_policies_service_days
        CHECK (
            minimum_service_days >= 0
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_policies_tenant
    ON leave_policies(tenant_id);

CREATE INDEX idx_leave_policies_leave_type
    ON leave_policies(leave_type_id);

CREATE INDEX idx_leave_policies_active
    ON leave_policies(is_active);

CREATE INDEX idx_leave_policies_code
    ON leave_policies(policy_code);

-- =============================================================================
-- UNIQUENESS
-- =============================================================================

CREATE UNIQUE INDEX uq_leave_policies_code
    ON leave_policies(
        tenant_id,
        policy_code
    )
    WHERE deleted_at IS NULL;

COMMIT;