-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 043_leave_balance_transactions.sql
-- Version     : 1.0
-- Description : Employee leave balance transaction ledger
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Records every movement against an employee leave balance.
--
-- Employee Leave Balance
--     = CURRENT aggregate balance for a leave period
--
-- Leave Balance Transaction
--     = WHY the balance changed
--
-- Supported transaction types:
--     accrual
--     deduction
--     carry_forward
--     adjustment
--     reversal
--
-- Leave requests may create deduction transactions after approval.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE BALANCE TRANSACTIONS
-- =============================================================================

CREATE TABLE leave_balance_transactions (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Balance
    ---------------------------------------------------------------------------

    employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Transaction Reference
    --
    -- System-generated unique reference for audit and reconciliation.
    -- Example:
    --     LBT-2026-000001
    ---------------------------------------------------------------------------

    transaction_number VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Transaction Type
    ---------------------------------------------------------------------------

    transaction_type identifier_code NOT NULL,

    ---------------------------------------------------------------------------
    -- Transaction Amount
    --
    -- Positive amount = credit to balance
    -- Negative amount = deduction from balance
    ---------------------------------------------------------------------------

    transaction_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Transaction Date
    ---------------------------------------------------------------------------

    transaction_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Source
    --
    -- Identifies the originating business record where applicable.
    --
    -- Examples:
    --     leave_request
    --     accrual
    --     carry_forward
    --     manual_adjustment
    --     reversal
    ---------------------------------------------------------------------------

    source_type identifier_code,

    source_id CHAR(26),

    ---------------------------------------------------------------------------
    -- Description
    ---------------------------------------------------------------------------

    description TEXT,

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

    CONSTRAINT fk_leave_balance_transactions_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_balance_transactions_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_balance_transactions_amount
        CHECK (
            transaction_days <> 0
        ),

    CONSTRAINT chk_leave_balance_transactions_type
        CHECK (
            transaction_type IN (
                'accrual',
                'deduction',
                'carry_forward',
                'adjustment',
                'reversal'
            )
        ),

    CONSTRAINT chk_leave_balance_transactions_source
        CHECK (
            (
                source_type IS NULL
                AND source_id IS NULL
            )
            OR
            (
                source_type IS NOT NULL
                AND source_id IS NOT NULL
            )
        ),

    CONSTRAINT uq_leave_balance_transactions_number
        UNIQUE (
            tenant_id,
            transaction_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_balance_transactions_balance
    ON leave_balance_transactions(
        employee_leave_balance_id
    );

CREATE INDEX idx_leave_balance_transactions_employee
    ON leave_balance_transactions(
        employee_id
    );

CREATE INDEX idx_leave_balance_transactions_date
    ON leave_balance_transactions(
        employee_id,
        transaction_date
    );

CREATE INDEX idx_leave_balance_transactions_type
    ON leave_balance_transactions(
        transaction_type
    );

CREATE INDEX idx_leave_balance_transactions_source
    ON leave_balance_transactions(
        source_type,
        source_id
    );

CREATE INDEX idx_leave_balance_transactions_active
    ON leave_balance_transactions(
        is_active
    );

COMMIT;