-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 051_leave_accrual_periods.sql
-- Version     : 1.0
-- Description : Leave accrual periods
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Defines concrete accrual periods used by the leave accrual engine.
--
-- 050 Leave Accrual Rules
--     = Defines HOW leave is accrued
--
-- 051 Leave Accrual Periods
--     = Defines WHEN an accrual period occurs
--
-- 043 Leave Balance Transactions
--     = Records the resulting balance movement
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL PERIODS
-- =============================================================================

CREATE TABLE leave_accrual_periods (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Accrual Rule
    ---------------------------------------------------------------------------

    leave_accrual_rule_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Assignment
    --
    -- The employee-specific assignment determines which employee receives
    -- the accrual generated for this period.
    ---------------------------------------------------------------------------

    employee_leave_assignment_id CHAR(26) NOT NULL,

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Period
    ---------------------------------------------------------------------------

    period_start DATE NOT NULL,

    period_end DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Expected Accrual
    ---------------------------------------------------------------------------

    scheduled_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Actual Accrual
    --
    -- Can differ from scheduled_days because of proration, service
    -- eligibility, termination, caps, or other business rules.
    ---------------------------------------------------------------------------

    accrued_days NUMERIC(10,2) NOT NULL DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Processing Status
    --
    -- pending
    -- processed
    -- skipped
    -- reversed
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Processing Timestamp
    ---------------------------------------------------------------------------

    processed_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Resulting Balance Transaction
    --
    -- Populated when the accrual engine successfully creates the
    -- corresponding balance transaction.
    ---------------------------------------------------------------------------

    leave_balance_transaction_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Processing Notes
    ---------------------------------------------------------------------------

    notes TEXT,

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

    CONSTRAINT fk_leave_accrual_periods_rule
        FOREIGN KEY (leave_accrual_rule_id)
        REFERENCES leave_accrual_rules(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_periods_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_periods_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_periods_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_accrual_periods_dates
        CHECK (
            period_end >= period_start
        ),

    CONSTRAINT chk_leave_accrual_periods_scheduled_days
        CHECK (
            scheduled_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_periods_accrued_days
        CHECK (
            accrued_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_periods_status
        CHECK (
            status IN (
                'pending',
                'processed',
                'skipped',
                'reversed'
            )
        ),

    CONSTRAINT chk_leave_accrual_periods_processed_at
        CHECK (
            (
                status IN ('pending', 'skipped')
                AND processed_at IS NULL
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND processed_at IS NOT NULL
            )
        ),

    CONSTRAINT chk_leave_accrual_periods_transaction
        CHECK (
            (
                status IN ('pending', 'skipped')
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    CONSTRAINT uq_leave_accrual_periods_assignment_period
        UNIQUE (
            tenant_id,
            employee_leave_assignment_id,
            period_start,
            period_end
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_periods_rule
    ON leave_accrual_periods(
        leave_accrual_rule_id
    );

CREATE INDEX idx_leave_accrual_periods_employee
    ON leave_accrual_periods(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_accrual_periods_assignment
    ON leave_accrual_periods(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_accrual_periods_period
    ON leave_accrual_periods(
        tenant_id,
        period_start,
        period_end
    );

CREATE INDEX idx_leave_accrual_periods_status
    ON leave_accrual_periods(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_accrual_periods_pending
    ON leave_accrual_periods(
        tenant_id,
        status,
        period_end
    );

COMMIT;