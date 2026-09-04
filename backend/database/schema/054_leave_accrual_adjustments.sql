-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 054_leave_accrual_adjustments.sql
-- Version     : 1.0
-- Description : Leave accrual adjustments
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records authorized manual adjustments to employee leave accruals.
--
-- 050 Leave Accrual Rules
--     = Defines automated accrual rules
--
-- 051 Leave Accrual Periods
--     = Defines employee accrual periods
--
-- 052 Leave Accrual Runs
--     = Defines batch accrual execution
--
-- 053 Leave Accrual Run Periods
--     = Tracks individual periods within a run
--
-- 054 Leave Accrual Adjustments
--     = Records authorized manual corrections
--
-- 043 Leave Balance Transactions
--     = Records the resulting balance movement
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL ADJUSTMENTS
-- =============================================================================

CREATE TABLE leave_accrual_adjustments (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Assignment
    ---------------------------------------------------------------------------

    employee_leave_assignment_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Balance
    ---------------------------------------------------------------------------

    employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Adjustment Identification
    ---------------------------------------------------------------------------

    adjustment_number VARCHAR(50) NOT NULL,

    adjustment_type identifier_code NOT NULL DEFAULT 'manual',

    ---------------------------------------------------------------------------
    -- Adjustment Amount
    --
    -- Positive value  = credit
    -- Negative value  = deduction
    ---------------------------------------------------------------------------

    adjustment_days NUMERIC(10,2) NOT NULL,

    adjustment_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Reason / Authorization
    ---------------------------------------------------------------------------

    reason TEXT NOT NULL,

    requested_by CHAR(26),

    approved_by CHAR(26),

    approved_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Processing Status
    --
    -- pending
    -- approved
    -- rejected
    -- applied
    -- cancelled
    -- reversed
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Resulting Balance Transaction
    ---------------------------------------------------------------------------

    leave_balance_transaction_id CHAR(26),

    applied_at TIMESTAMPTZ,

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

    CONSTRAINT fk_leave_accrual_adjustments_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_adjustments_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_adjustments_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_adjustments_requested_by
        FOREIGN KEY (requested_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_adjustments_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_adjustments_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Checks
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_adjustments_number
        CHECK (
            LENGTH(TRIM(adjustment_number)) > 0
        ),

    CONSTRAINT chk_leave_accrual_adjustments_days
        CHECK (
            adjustment_days <> 0
        ),

    CONSTRAINT chk_leave_accrual_adjustments_reason
        CHECK (
            LENGTH(TRIM(reason)) > 0
        ),

    CONSTRAINT chk_leave_accrual_adjustments_type
        CHECK (
            adjustment_type IN (
                'manual',
                'correction',
                'administrative',
                'carry_forward',
                'reversal'
            )
        ),

    CONSTRAINT chk_leave_accrual_adjustments_status
        CHECK (
            status IN (
                'pending',
                'approved',
                'rejected',
                'applied',
                'cancelled',
                'reversed'
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_adjustments_approval
        CHECK (
            (
                status IN ('pending', 'rejected', 'cancelled')
                AND approved_by IS NULL
                AND approved_at IS NULL
            )
            OR
            (
                status IN ('approved', 'applied', 'reversed')
                AND approved_by IS NOT NULL
                AND approved_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Applied consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_adjustments_applied
        CHECK (
            (
                status IN (
                    'pending',
                    'approved',
                    'rejected',
                    'cancelled'
                )
                AND applied_at IS NULL
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('applied', 'reversed')
                AND applied_at IS NOT NULL
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    CONSTRAINT chk_leave_accrual_adjustments_approval_order
        CHECK (
            approved_at IS NULL
            OR approved_at >= created_at
        ),

    CONSTRAINT chk_leave_accrual_adjustments_applied_order
        CHECK (
            applied_at IS NULL
            OR (
                approved_at IS NOT NULL
                AND applied_at >= approved_at
            )
        ),

    ---------------------------------------------------------------------------
    -- One adjustment number per tenant.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_accrual_adjustments_number
        UNIQUE (
            tenant_id,
            adjustment_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_adjustments_employee
    ON leave_accrual_adjustments(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_accrual_adjustments_assignment
    ON leave_accrual_adjustments(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_accrual_adjustments_balance
    ON leave_accrual_adjustments(
        employee_leave_balance_id
    );

CREATE INDEX idx_leave_accrual_adjustments_status
    ON leave_accrual_adjustments(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_accrual_adjustments_date
    ON leave_accrual_adjustments(
        tenant_id,
        adjustment_date
    );

CREATE INDEX idx_leave_accrual_adjustments_requested_by
    ON leave_accrual_adjustments(
        requested_by
    );

CREATE INDEX idx_leave_accrual_adjustments_approved_by
    ON leave_accrual_adjustments(
        approved_by
    );

CREATE INDEX idx_leave_accrual_adjustments_transaction
    ON leave_accrual_adjustments(
        leave_balance_transaction_id
    );

CREATE INDEX idx_leave_accrual_adjustments_active
    ON leave_accrual_adjustments(
        tenant_id,
        is_active
    );

COMMIT;