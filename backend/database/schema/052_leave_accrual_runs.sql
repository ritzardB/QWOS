-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 052_leave_accrual_runs.sql
-- Version     : 1.0
-- Description : Leave accrual processing runs
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records each execution of the leave accrual engine.
--
-- 050 Leave Accrual Rules
--     = Defines HOW leave is accrued
--
-- 051 Leave Accrual Periods
--     = Defines the employee-specific periods to process
--
-- 052 Leave Accrual Runs
--     = Records the batch execution and processing result
--
-- 043 Leave Balance Transactions
--     = Records the resulting balance movements
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL RUNS
-- =============================================================================

CREATE TABLE leave_accrual_runs (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Run Identification
    ---------------------------------------------------------------------------

    run_number VARCHAR(50) NOT NULL,

    run_type identifier_code NOT NULL DEFAULT 'scheduled',

    ---------------------------------------------------------------------------
    -- Processing Period
    ---------------------------------------------------------------------------

    period_start DATE NOT NULL,

    period_end DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Execution
    ---------------------------------------------------------------------------

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    completed_at TIMESTAMPTZ,

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Processing Statistics
    ---------------------------------------------------------------------------

    total_periods INTEGER NOT NULL DEFAULT 0,

    processed_periods INTEGER NOT NULL DEFAULT 0,

    skipped_periods INTEGER NOT NULL DEFAULT 0,

    failed_periods INTEGER NOT NULL DEFAULT 0,

    total_accrued_days NUMERIC(14,2) NOT NULL DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Error / Execution Information
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
    -- Constraints
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_runs_dates
        CHECK (
            period_end >= period_start
        ),

    CONSTRAINT chk_leave_accrual_runs_status
        CHECK (
            status IN (
                'pending',
                'running',
                'completed',
                'completed_with_errors',
                'failed',
                'cancelled'
            )
        ),

    CONSTRAINT chk_leave_accrual_runs_type
        CHECK (
            run_type IN (
                'scheduled',
                'manual',
                'reprocessing'
            )
        ),

    CONSTRAINT chk_leave_accrual_runs_completed_at
        CHECK (
            (
                status IN ('pending', 'running')
                AND completed_at IS NULL
            )
            OR
            (
                status IN (
                    'completed',
                    'completed_with_errors',
                    'failed',
                    'cancelled'
                )
                AND completed_at IS NOT NULL
            )
        ),

    CONSTRAINT chk_leave_accrual_runs_total_periods
        CHECK (
            total_periods >= 0
        ),

    CONSTRAINT chk_leave_accrual_runs_processed_periods
        CHECK (
            processed_periods >= 0
        ),

    CONSTRAINT chk_leave_accrual_runs_skipped_periods
        CHECK (
            skipped_periods >= 0
        ),

    CONSTRAINT chk_leave_accrual_runs_failed_periods
        CHECK (
            failed_periods >= 0
        ),

    CONSTRAINT chk_leave_accrual_runs_accrued_days
        CHECK (
            total_accrued_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_runs_period_counts
        CHECK (
            processed_periods
            + skipped_periods
            + failed_periods
            <= total_periods
        ),

    CONSTRAINT chk_leave_accrual_runs_error
        CHECK (
            (
                status NOT IN ('failed', 'completed_with_errors')
                AND error_message IS NULL
            )
            OR
            (
                status IN ('failed', 'completed_with_errors')
                AND error_message IS NOT NULL
            )
        ),

    CONSTRAINT uq_leave_accrual_runs_number
        UNIQUE (
            tenant_id,
            run_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_runs_period
    ON leave_accrual_runs(
        tenant_id,
        period_start,
        period_end
    );

CREATE INDEX idx_leave_accrual_runs_status
    ON leave_accrual_runs(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_accrual_runs_type
    ON leave_accrual_runs(
        tenant_id,
        run_type
    );

CREATE INDEX idx_leave_accrual_runs_started
    ON leave_accrual_runs(
        tenant_id,
        started_at
    );

CREATE INDEX idx_leave_accrual_runs_active
    ON leave_accrual_runs(
        tenant_id,
        is_active
    );

COMMIT;