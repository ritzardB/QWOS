-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 050_leave_accrual_rules.sql
-- Version     : 1.0
-- Description : Leave accrual rules
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines how leave entitlement is accrued under a leave policy.
--
-- Leave Policy
--     = HOW the leave is governed
--
-- Leave Accrual Rule
--     = HOW leave is earned over time
--
-- Leave Balance
--     = CURRENT aggregate entitlement/balance
--
-- Leave Balance Transaction
--     = INDIVIDUAL movement affecting the balance
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL RULES
-- =============================================================================

CREATE TABLE leave_accrual_rules (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Policy
    ---------------------------------------------------------------------------

    leave_policy_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Rule Identification
    ---------------------------------------------------------------------------

    rule_code VARCHAR(50) NOT NULL,

    rule_name VARCHAR(150) NOT NULL,

    description TEXT,

    ---------------------------------------------------------------------------
    -- Accrual Method
    --
    -- fixed       = fixed amount awarded per accrual period
    -- annual      = annual entitlement
    -- monthly     = monthly entitlement
    -- pro_rata    = calculated according to service period
    -- anniversary = entitlement based on employee anniversary
    ---------------------------------------------------------------------------

    accrual_method identifier_code NOT NULL DEFAULT 'monthly',

    ---------------------------------------------------------------------------
    -- Accrual Frequency
    --
    -- monthly
    -- quarterly
    -- annually
    -- anniversary
    ---------------------------------------------------------------------------

    accrual_frequency identifier_code NOT NULL DEFAULT 'monthly',

    ---------------------------------------------------------------------------
    -- Accrual Amount
    ---------------------------------------------------------------------------

    accrual_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Maximum Accrual
    --
    -- Optional cap on accumulated accrual for the applicable period.
    ---------------------------------------------------------------------------

    maximum_accrual_days NUMERIC(10,2),

    ---------------------------------------------------------------------------
    -- Waiting / Service Requirement
    --
    -- Number of completed service days before accrual begins.
    ---------------------------------------------------------------------------

    minimum_service_days INTEGER NOT NULL DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Proration
    --
    -- Determines whether the accrual should be prorated for partial periods.
    ---------------------------------------------------------------------------

    prorate_on_join BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    prorate_on_termination BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Accrual Timing
    --
    -- beginning_of_period
    -- end_of_period
    -- anniversary
    ---------------------------------------------------------------------------

    accrual_timing identifier_code
        NOT NULL
        DEFAULT 'end_of_period',

    ---------------------------------------------------------------------------
    -- Carry Forward
    --
    -- Whether unused accrued leave can continue into the next period.
    ---------------------------------------------------------------------------

    carry_forward_allowed BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    carry_forward_days NUMERIC(10,2),

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    effective_from DATE NOT NULL,

    effective_until DATE,

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

    CONSTRAINT fk_leave_accrual_rules_policy
        FOREIGN KEY (leave_policy_id)
        REFERENCES leave_policies(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_accrual_rules_code
        CHECK (
            LENGTH(TRIM(rule_code)) > 0
        ),

    CONSTRAINT chk_leave_accrual_rules_name
        CHECK (
            LENGTH(TRIM(rule_name)) > 0
        ),

    CONSTRAINT chk_leave_accrual_rules_amount
        CHECK (
            accrual_days > 0
        ),

    CONSTRAINT chk_leave_accrual_rules_maximum
        CHECK (
            maximum_accrual_days IS NULL
            OR maximum_accrual_days >= accrual_days
        ),

    CONSTRAINT chk_leave_accrual_rules_service
        CHECK (
            minimum_service_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_rules_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT chk_leave_accrual_rules_method
        CHECK (
            accrual_method IN (
                'fixed',
                'annual',
                'monthly',
                'pro_rata',
                'anniversary'
            )
        ),

    CONSTRAINT chk_leave_accrual_rules_frequency
        CHECK (
            accrual_frequency IN (
                'monthly',
                'quarterly',
                'annually',
                'anniversary'
            )
        ),

    CONSTRAINT chk_leave_accrual_rules_timing
        CHECK (
            accrual_timing IN (
                'beginning_of_period',
                'end_of_period',
                'anniversary'
            )
        ),

    CONSTRAINT chk_leave_accrual_rules_carry_forward
        CHECK (
            (
                carry_forward_allowed = FALSE
                AND carry_forward_days IS NULL
            )
            OR
            (
                carry_forward_allowed = TRUE
                AND carry_forward_days IS NOT NULL
                AND carry_forward_days >= 0
            )
        ),

    CONSTRAINT uq_leave_accrual_rules_code
        UNIQUE (
            tenant_id,
            rule_code,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_rules_policy
    ON leave_accrual_rules(
        leave_policy_id
    );

CREATE INDEX idx_leave_accrual_rules_active
    ON leave_accrual_rules(
        tenant_id,
        is_active
    );

CREATE INDEX idx_leave_accrual_rules_effective
    ON leave_accrual_rules(
        leave_policy_id,
        effective_from,
        effective_until
    );

CREATE INDEX idx_leave_accrual_rules_method
    ON leave_accrual_rules(
        accrual_method,
        accrual_frequency
    );

COMMIT;