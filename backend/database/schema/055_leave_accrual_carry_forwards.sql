-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 055_leave_accrual_carry_forwards.sql
-- Version     : 1.0
-- Description : Leave accrual carry-forward records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records leave days carried from one balance period into another.
--
-- 050 Leave Accrual Rules
--     = Defines whether and how much leave may be carried forward
--
-- 051 Leave Accrual Periods
--     = Defines accrual periods
--
-- 054 Leave Accrual Adjustments
--     = Handles authorized manual corrections
--
-- 055 Leave Accrual Carry Forwards
--     = Records policy-driven carry-forward movements
--
-- 043 Leave Balance Transactions
--     = Records the resulting balance movement
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE ACCRUAL CARRY FORWARDS
-- =============================================================================

CREATE TABLE leave_accrual_carry_forwards (

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
    -- Source Balance
    --
    -- Balance from which unused leave is being carried forward.
    ---------------------------------------------------------------------------

    source_employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Destination Balance
    --
    -- Balance receiving the carried-forward leave.
    ---------------------------------------------------------------------------

    destination_employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Source / Destination Periods
    ---------------------------------------------------------------------------

    source_period_start DATE NOT NULL,

    source_period_end DATE NOT NULL,

    destination_period_start DATE NOT NULL,

    destination_period_end DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Carry-Forward Amount
    ---------------------------------------------------------------------------

    eligible_days NUMERIC(10,2) NOT NULL,

    carried_forward_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Expiration
    --
    -- Optional expiration date for carried-forward entitlement.
    ---------------------------------------------------------------------------

    expires_at DATE,

    ---------------------------------------------------------------------------
    -- Processing
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    processed_at TIMESTAMPTZ,

    ---------------------------------------------------------------------------
    -- Resulting Balance Transaction
    ---------------------------------------------------------------------------

    leave_balance_transaction_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Explanation
    ---------------------------------------------------------------------------

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

    CONSTRAINT fk_leave_accrual_carry_forwards_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_carry_forwards_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_carry_forwards_source_balance
        FOREIGN KEY (source_employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_carry_forwards_destination_balance
        FOREIGN KEY (destination_employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_accrual_carry_forwards_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Period Checks
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_source_dates
        CHECK (
            source_period_end >= source_period_start
        ),

    CONSTRAINT chk_leave_accrual_carry_forwards_destination_dates
        CHECK (
            destination_period_end >= destination_period_start
        ),

    CONSTRAINT chk_leave_accrual_carry_forwards_period_order
        CHECK (
            destination_period_start > source_period_end
        ),

    ---------------------------------------------------------------------------
    -- Amount Checks
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_eligible_days
        CHECK (
            eligible_days >= 0
        ),

    CONSTRAINT chk_leave_accrual_carry_forwards_days
        CHECK (
            carried_forward_days > 0
        ),

    CONSTRAINT chk_leave_accrual_carry_forwards_limit
        CHECK (
            carried_forward_days <= eligible_days
        ),

    ---------------------------------------------------------------------------
    -- Expiration
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_expiration
        CHECK (
            expires_at IS NULL
            OR expires_at >= destination_period_start
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_status
        CHECK (
            status IN (
                'pending',
                'processed',
                'expired',
                'reversed',
                'cancelled'
            )
        ),

    ---------------------------------------------------------------------------
    -- Processing Consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_processed
        CHECK (
            (
                status IN ('pending', 'cancelled')
                AND processed_at IS NULL
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('processed', 'expired', 'reversed')
                AND processed_at IS NOT NULL
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Prevent self-transfer.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_accrual_carry_forwards_balances
        CHECK (
            source_employee_leave_balance_id
            <> destination_employee_leave_balance_id
        ),

    ---------------------------------------------------------------------------
    -- One carry-forward per source/destination balance pair.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_accrual_carry_forwards_balances
        UNIQUE (
            tenant_id,
            source_employee_leave_balance_id,
            destination_employee_leave_balance_id
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_accrual_carry_forwards_employee
    ON leave_accrual_carry_forwards(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_accrual_carry_forwards_assignment
    ON leave_accrual_carry_forwards(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_accrual_carry_forwards_source
    ON leave_accrual_carry_forwards(
        source_employee_leave_balance_id
    );

CREATE INDEX idx_leave_accrual_carry_forwards_destination
    ON leave_accrual_carry_forwards(
        destination_employee_leave_balance_id
    );

CREATE INDEX idx_leave_accrual_carry_forwards_status
    ON leave_accrual_carry_forwards(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_accrual_carry_forwards_expiration
    ON leave_accrual_carry_forwards(
        tenant_id,
        expires_at
    );

CREATE INDEX idx_leave_accrual_carry_forwards_transaction
    ON leave_accrual_carry_forwards(
        leave_balance_transaction_id
    );

CREATE INDEX idx_leave_accrual_carry_forwards_active
    ON leave_accrual_carry_forwards(
        tenant_id,
        is_active
    );

COMMIT;