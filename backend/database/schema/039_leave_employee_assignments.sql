-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 039_leave_employee_assignments.sql
-- Version     : 1.0
-- Description : Effective-dated employee leave policy assignments
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Assigns a leave policy to an employee for a defined effective period.
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
-- Leave balances are maintained separately.
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- EMPLOYEE LEAVE ASSIGNMENTS
-- =============================================================================

CREATE TABLE employee_leave_assignments (

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
    -- Leave Policy
    ---------------------------------------------------------------------------

    leave_policy_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Effective Dates
    ---------------------------------------------------------------------------

    effective_from DATE NOT NULL,

    effective_until DATE,

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

    CONSTRAINT fk_employee_leave_assignments_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_employee_leave_assignments_policy
        FOREIGN KEY (leave_policy_id)
        REFERENCES leave_policies(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_employee_leave_assignments_dates
        CHECK (
            effective_until IS NULL
            OR effective_until >= effective_from
        ),

    CONSTRAINT uq_employee_leave_assignments_start
        UNIQUE (
            tenant_id,
            employee_id,
            effective_from
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_employee_leave_assignments_employee
    ON employee_leave_assignments(employee_id);

CREATE INDEX idx_employee_leave_assignments_policy
    ON employee_leave_assignments(leave_policy_id);

CREATE INDEX idx_employee_leave_assignments_active
    ON employee_leave_assignments(is_active);

CREATE INDEX idx_employee_leave_assignments_effective
    ON employee_leave_assignments(
        employee_id,
        effective_from,
        effective_until
    );

COMMIT;