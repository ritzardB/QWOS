-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 057_leave_balance_adjustments.sql
-- Version     : 1.0
-- Description : Leave balance adjustments
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records authorized manual adjustments made directly to an employee's
-- leave balance.
--
-- 040 Employee Leave Balances
--     = Current aggregate balance
--
-- 043 Leave Balance Transactions
--     = Immutable balance movement ledger
--
-- 054 Leave Accrual Adjustments
--     = Corrections to accrual calculations
--
-- 057 Leave Balance Adjustments
--     = Direct authorized balance corrections
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE BALANCE ADJUSTMENTS
-- =============================================================================

CREATE TABLE leave_balance_adjustments (

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
    -- Positive value = credit
    -- Negative value = deduction
    ---------------------------------------------------------------------------

    adjustment_days NUMERIC(10,2) NOT NULL,

    adjustment_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Reason
    ---------------------------------------------------------------------------

    reason TEXT NOT NULL,

    ---------------------------------------------------------------------------
    -- Authorization
    ---------------------------------------------------------------------------

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

    CONSTRAINT fk_leave_balance_adjustments_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_adjustments_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_adjustments_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_adjustments_requested_by
        FOREIGN KEY (requested_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_adjustments_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_adjustments_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Identification
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_number
        CHECK (
            LENGTH(TRIM(adjustment_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Adjustment Amount
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_days
        CHECK (
            adjustment_days <> 0
        ),

    ---------------------------------------------------------------------------
    -- Reason
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_reason
        CHECK (
            LENGTH(TRIM(reason)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Adjustment Type
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_type
        CHECK (
            adjustment_type IN (
                'manual',
                'correction',
                'administrative',
                'carry_forward',
                'reversal'
            )
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_status
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
    -- Approval Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_approval
        CHECK (
            (
                status IN (
                    'pending',
                    'rejected',
                    'cancelled'
                )
                AND approved_by IS NULL
                AND approved_at IS NULL
            )
            OR
            (
                status IN (
                    'approved',
                    'applied',
                    'reversed'
                )
                AND approved_by IS NOT NULL
                AND approved_at IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Applied Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_applied
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
                status IN (
                    'applied',
                    'reversed'
                )
                AND applied_at IS NOT NULL
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Approval must occur after creation.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_approval_order
        CHECK (
            approved_at IS NULL
            OR approved_at >= created_at
        ),

    ---------------------------------------------------------------------------
    -- Application must occur after approval.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_adjustments_applied_order
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

    CONSTRAINT uq_leave_balance_adjustments_number
        UNIQUE (
            tenant_id,
            adjustment_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_balance_adjustments_employee
    ON leave_balance_adjustments(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_balance_adjustments_assignment
    ON leave_balance_adjustments(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_balance_adjustments_balance
    ON leave_balance_adjustments(
        employee_leave_balance_id
    );

CREATE INDEX idx_leave_balance_adjustments_status
    ON leave_balance_adjustments(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_balance_adjustments_date
    ON leave_balance_adjustments(
        tenant_id,
        adjustment_date
    );

CREATE INDEX idx_leave_balance_adjustments_requested_by
    ON leave_balance_adjustments(
        requested_by
    );

CREATE INDEX idx_leave_balance_adjustments_approved_by
    ON leave_balance_adjustments(
        approved_by
    );

CREATE INDEX idx_leave_balance_adjustments_transaction
    ON leave_balance_adjustments(
        leave_balance_transaction_id
    );

CREATE INDEX idx_leave_balance_adjustments_active
    ON leave_balance_adjustments(
        tenant_id,
        is_active
    );

COMMIT;