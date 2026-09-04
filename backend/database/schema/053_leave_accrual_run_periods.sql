-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 053_leave_accrual_run_periods.sql
-- Version     : 1.0
-- Description : Leave accrual run period processing records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Links an accrual processing run to the individual employee accrual periods
-- processed during that run.
--
-- 050 Leave Accrual Rules
--     = Defines HOW leave is accrued
--
-- 051 Leave Accrual Periods
--     = Defines WHEN an employee accrues leave
--
-- 052 Leave Accrual Runs
--     = Defines the batch execution
--
-- 053 Leave Accrual Run Periods
--     = Tracks each period within the batch execution
--
-- 043 Leave Balance Transactions
--     = Records the resulting balance movement
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL RUN PERIODS
-- =============================================================================

CREATE TABLE leave_accrual_run_periods (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Accrual Run
    ---------------------------------------------------------------------------

    leave_accrual_run_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Accrual Period
    ---------------------------------------------------------------------------

    leave_accrual_period_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Context
    --
    -- Denormalized intentionally for efficient reporting and tenant-scoped
    -- processing.
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Processing
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Result
    ---------------------------------------------------------------------------

    scheduled_days NUMERIC(10,2) NOT NULL DEFAULT 0,

    accrued_days NUMERIC(10,2) NOT NULL DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Resulting Transaction
    ---------------------------------------------------------------------------

    leave_balance_transaction_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Error / Processing Information
    ---------------------------------------------------------------------------

    error_message TEXT,

    notes TEXT,

    ---------------------------------------------------------------------------
    -- Lifecycle
    ---------------------------------------------------------------------------

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    ---------------------------------------------------------------------------
    -- Audit
    ---------------------------------------------------------------------------

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_by CHAR(26),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_by CHAR(26),

    deleted_at TIMESTAMPTZ,

    deleted_by CHAR(26),

    ---------------------------------------------------------------------------
    -- Concurrency
    ---------------------------------------------------------------------------

    version INTEGER NOT NULL DEFAULT 1,

    ---------------------------------------------------------------------------
    -- Foreign Keys
    ---------------------------------------------------------------------------

    CONSTRAINT fk_leave_accrual_run_periods_run
        FOREIGN KEY (leave_accrual_run_id)
        REFERENCES leave_accrual_runs(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_run_periods_period
        FOREIGN KEY (leave_accrual_period_id)
        REFERENCES leave_accrual_periods(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_run_periods_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_run_periods_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Checks
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_run_periods_status
        CHECK (
            status IN (
                'pending',
                'running',
                'processed',
                'skipped',
                'failed',
                'reversed'
            )
        ),

    CONSTRAINT chk_leave_accrual_run_periods_dates
        CHECK (
            (
                status IN ('pending', 'skipped')
                AND started_at IS NULL
                AND completed_at IS NULL
            )
            OR
            (
                status = 'running'
                AND started_at IS NOT NULL
                AND completed_at IS NULL
            )
            OR
            (
                status IN ('processed', 'failed', 'reversed')
                AND started_at IS NOT NULL
                AND completed_at IS NOT NULL
            )
        ),

    CONSTRAINT chk_leave_accrual_run_periods_completion
        CHECK (
            completed_at IS NULL
            OR completed_at >= started_at
        ),

    CONSTRAINT chk_leave_accrual_run_periods_scheduled_days
        CHECK (
            scheduled_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_run_periods_accrued_days
        CHECK (
            accrued_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_run_periods_transaction
        CHECK (
            (
                status IN ('pending', 'running', 'skipped', 'failed')
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    CONSTRAINT chk_leave_accrual_run_periods_error
        CHECK (
            (
                status <> 'failed'
                AND error_message IS NULL
            )
            OR
            (
                status = 'failed'
                AND error_message IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- One period may be processed only once per run.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_accrual_run_periods_run_period
        UNIQUE (
            tenant_id,
            leave_accrual_run_id,
            leave_accrual_period_id
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_run_periods_run
    ON leave_accrual_run_periods(
        tenant_id,
        leave_accrual_run_id
    );

CREATE INDEX idx_leave_accrual_run_periods_period
    ON leave_accrual_run_periods(
        leave_accrual_period_id
    );

CREATE INDEX idx_leave_accrual_run_periods_employee
    ON leave_accrual_run_periods(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_accrual_run_periods_status
    ON leave_accrual_run_periods(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_accrual_run_periods_pending
    ON leave_accrual_run_periods(
        tenant_id,
        status,
        created_at
    );

CREATE INDEX idx_leave_accrual_run_periods_transaction
    ON leave_accrual_run_periods(
        leave_balance_transaction_id
    );

COMMIT;