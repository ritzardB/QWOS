-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 056_leave_balance_expirations.sql
-- Version     : 1.0
-- Description : Leave balance expiration records
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Tracks leave entitlement that is subject to expiration.
--
-- 055 Leave Accrual Carry Forwards
--     = Records leave carried into a subsequent balance period
--
-- 056 Leave Balance Expirations
--     = Records entitlement subject to expiration
--
-- 043 Leave Balance Transactions
--     = Records the resulting expiration/reversal movement
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE BALANCE EXPIRATIONS
-- =============================================================================

CREATE TABLE leave_balance_expirations (

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
    --
    -- Balance containing the entitlement subject to expiration.
    ---------------------------------------------------------------------------

    employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Carry Forward Source
    --
    -- Nullable because an expiring balance does not necessarily originate
    -- from a carry-forward.
    ---------------------------------------------------------------------------

    leave_accrual_carry_forward_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Expiration Identification
    ---------------------------------------------------------------------------

    expiration_number VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Entitlement
    ---------------------------------------------------------------------------

    eligible_days NUMERIC(10,2) NOT NULL,

    expired_days NUMERIC(10,2) NOT NULL DEFAULT 0,

    ---------------------------------------------------------------------------
    -- Expiration Date
    ---------------------------------------------------------------------------

    expiration_date DATE NOT NULL,

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

    CONSTRAINT fk_leave_balance_expirations_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_expirations_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_expirations_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_expirations_carry_forward
        FOREIGN KEY (leave_accrual_carry_forward_id)
        REFERENCES leave_accrual_carry_forwards(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_expirations_transaction
        FOREIGN KEY (leave_balance_transaction_id)
        REFERENCES leave_balance_transactions(id)
        ON DELETE RESTRICT,

    ---------------------------------------------------------------------------
    -- Identification
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_number
        CHECK (
            LENGTH(TRIM(expiration_number)) > 0
        ),

    ---------------------------------------------------------------------------
    -- Amounts
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_eligible_days
        CHECK (
            eligible_days > 0
        ),

    CONSTRAINT chk_leave_balance_expirations_expired_days
        CHECK (
            expired_days >= 0
        ),

    CONSTRAINT chk_leave_balance_expirations_limit
        CHECK (
            expired_days <= eligible_days
        ),

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_status
        CHECK (
            status IN (
                'pending',
                'processed',
                'cancelled',
                'reversed'
            )
        ),

    ---------------------------------------------------------------------------
    -- Processing consistency
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_processed
        CHECK (
            (
                status IN ('pending', 'cancelled')
                AND processed_at IS NULL
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND processed_at IS NOT NULL
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- Processed expiration must contain expired days.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_processed_days
        CHECK (
            (
                status IN ('pending', 'cancelled')
                AND expired_days = 0
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND expired_days > 0
            )
        ),

    ---------------------------------------------------------------------------
    -- Transaction must represent a balance movement.
    ---------------------------------------------------------------------------

    CONSTRAINT chk_leave_balance_expirations_transaction
        CHECK (
            (
                status IN ('pending', 'cancelled')
                AND leave_balance_transaction_id IS NULL
            )
            OR
            (
                status IN ('processed', 'reversed')
                AND leave_balance_transaction_id IS NOT NULL
            )
        ),

    ---------------------------------------------------------------------------
    -- A carry-forward may generate only one expiration record.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_balance_expirations_carry_forward
        UNIQUE (
            tenant_id,
            leave_accrual_carry_forward_id
        ),

    ---------------------------------------------------------------------------
    -- Expiration number is unique within a tenant.
    ---------------------------------------------------------------------------

    CONSTRAINT uq_leave_balance_expirations_number
        UNIQUE (
            tenant_id,
            expiration_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_balance_expirations_employee
    ON leave_balance_expirations(
        tenant_id,
        employee_id
    );

CREATE INDEX idx_leave_balance_expirations_assignment
    ON leave_balance_expirations(
        employee_leave_assignment_id
    );

CREATE INDEX idx_leave_balance_expirations_balance
    ON leave_balance_expirations(
        employee_leave_balance_id
    );

CREATE INDEX idx_leave_balance_expirations_carry_forward
    ON leave_balance_expirations(
        leave_accrual_carry_forward_id
    );

CREATE INDEX idx_leave_balance_expirations_date
    ON leave_balance_expirations(
        tenant_id,
        expiration_date
    );

CREATE INDEX idx_leave_balance_expirations_status
    ON leave_balance_expirations(
        tenant_id,
        status
    );

CREATE INDEX idx_leave_balance_expirations_pending
    ON leave_balance_expirations(
        tenant_id,
        status,
        expiration_date
    );

CREATE INDEX idx_leave_balance_expirations_transaction
    ON leave_balance_expirations(
        leave_balance_transaction_id
    );

CREATE INDEX idx_leave_balance_expirations_active
    ON leave_balance_expirations(
        tenant_id,
        is_active
    );

COMMIT;