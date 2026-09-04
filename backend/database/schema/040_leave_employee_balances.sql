-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 040_leave_employee_balances.sql
-- Version     : 1.0
-- Description : Employee leave balances and entitlement tracking
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores the leave entitlement and balance for an employee under an assigned
-- leave policy for a specific leave period.
--
-- Leave Type
--     = WHAT kind of leave exists
--
-- Leave Policy
--     = HOW the leave is governed
--
-- Employee Leave Assignment
--     = WHICH policy applies to WHICH employee
--
-- Employee Leave Balance
--     = HOW MUCH leave the employee has available
--
-- Leave Requests are maintained separately.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE LEAVE BALANCES
-- =============================================================================

CREATE TABLE employee_leave_balances (

    ---------------------------------------------------------------------------
    -- Primary Key
    ---------------------------------------------------------------------------

    id CHAR(26) PRIMARY KEY,

    ---------------------------------------------------------------------------
    -- Tenant
    ---------------------------------------------------------------------------

    tenant_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee Leave Assignment
    ---------------------------------------------------------------------------

    employee_leave_assignment_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Employee
    --
    -- Kept explicitly for efficient tenant/employee reporting and querying.
    -- The assignment remains the source of the policy relationship.
    ---------------------------------------------------------------------------

    employee_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Period
    ---------------------------------------------------------------------------

    period_start DATE NOT NULL,

    period_end DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Balance
    --
    -- entitlement_days = total entitlement for the period
    -- carried_forward_days = amount brought forward from a previous period
    -- accrued_days = amount earned during the period
    -- used_days = approved leave consumed
    -- adjustment_days = authorized manual/system adjustment
    --
    -- available_days is derived from these values and therefore is not stored.
    ---------------------------------------------------------------------------

    entitlement_days NUMERIC(10,2)
        NOT NULL
        DEFAULT 0,

    carried_forward_days NUMERIC(10,2)
        NOT NULL
        DEFAULT 0,

    accrued_days NUMERIC(10,2)
        NOT NULL
        DEFAULT 0,

    used_days NUMERIC(10,2)
        NOT NULL
        DEFAULT 0,

    adjustment_days NUMERIC(10,2)
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

    CONSTRAINT fk_employee_leave_balances_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_leave_balances_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_leave_balances_period
        CHECK (
            period_end >= period_start
        ),

    CONSTRAINT chk_employee_leave_balances_entitlement
        CHECK (
            entitlement_days >= 0
        ),

    CONSTRAINT chk_employee_leave_balances_carried_forward
        CHECK (
            carried_forward_days >= 0
        ),

    CONSTRAINT chk_employee_leave_balances_accrued
        CHECK (
            accrued_days >= 0
        ),

    CONSTRAINT chk_employee_leave_balances_used
        CHECK (
            used_days >= 0
        ),

    CONSTRAINT uq_employee_leave_balances_period
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

CREATE INDEX idx_employee_leave_balances_employee
    ON employee_leave_balances(employee_id);

CREATE INDEX idx_employee_leave_balances_assignment
    ON employee_leave_balances(employee_leave_assignment_id);

CREATE INDEX idx_employee_leave_balances_period
    ON employee_leave_balances(
        employee_id,
        period_start,
        period_end
    );

CREATE INDEX idx_employee_leave_balances_active
    ON employee_leave_balances(is_active);

COMMIT;