-- =============================================================================
-- Quantum Workforce OS (QWOS)
-- QuantumDB
-- =============================================================================
--
-- File        : 041_leave_requests.sql
-- Version     : 1.0
-- Description : Employee leave requests
--
-- Author      : Richard Balabarcon
-- Architecture: Quantum Database Standard (QDS)
--
-- =============================================================================
--
-- Purpose
-- -----------------------------------------------------------------------------
-- Stores employee requests for leave.
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
--     = HOW MUCH leave the employee has
--
-- Leave Request
--     = WHAT leave the employee is requesting
--
-- Leave Approval
--     = WHO approves or rejects the request
--
-- =============================================================================

BEGIN;

-- =============================================================================
-- LEAVE REQUESTS
-- =============================================================================

CREATE TABLE leave_requests (

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
    -- Identifies the balance period against which the request is evaluated.
    ---------------------------------------------------------------------------

    employee_leave_balance_id CHAR(26) NOT NULL,

    ---------------------------------------------------------------------------
    -- Request Reference
    --
    -- System-generated human-readable request number.
    -- Example: LV-2026-000001
    ---------------------------------------------------------------------------

    request_number VARCHAR(50) NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Dates
    ---------------------------------------------------------------------------

    leave_start_date DATE NOT NULL,

    leave_end_date DATE NOT NULL,

    ---------------------------------------------------------------------------
    -- Leave Duration
    --
    -- Supports partial-day leave.
    ---------------------------------------------------------------------------

    requested_days NUMERIC(10,2) NOT NULL,

    ---------------------------------------------------------------------------
    -- Partial-Day Support
    --
    -- full_day  = complete working day(s)
    -- half_day  = half-day leave
    -- partial   = another approved fraction
    ---------------------------------------------------------------------------

    duration_type identifier_code NOT NULL DEFAULT 'full_day',

    ---------------------------------------------------------------------------
    -- Reason
    ---------------------------------------------------------------------------

    reason TEXT,

    ---------------------------------------------------------------------------
    -- Request Status
    --
    -- pending   = awaiting approval
    -- approved  = approved
    -- rejected  = rejected
    -- cancelled = cancelled by employee/authorized user
    -- withdrawn = withdrawn before completion
    ---------------------------------------------------------------------------

    status identifier_code NOT NULL DEFAULT 'pending',

    ---------------------------------------------------------------------------
    -- Submission
    ---------------------------------------------------------------------------

    submitted_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

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

    CONSTRAINT fk_leave_requests_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_requests_assignment
        FOREIGN KEY (employee_leave_assignment_id)
        REFERENCES employee_leave_assignments(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_leave_requests_balance
        FOREIGN KEY (employee_leave_balance_id)
        REFERENCES employee_leave_balances(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_leave_requests_dates
        CHECK (
            leave_end_date >= leave_start_date
        ),

    CONSTRAINT chk_leave_requests_days
        CHECK (
            requested_days > 0
        ),

    CONSTRAINT chk_leave_requests_duration_type
        CHECK (
            duration_type IN (
                'full_day',
                'half_day',
                'partial'
            )
        ),

    CONSTRAINT chk_leave_requests_status
        CHECK (
            status IN (
                'pending',
                'approved',
                'rejected',
                'cancelled',
                'withdrawn'
            )
        ),

    CONSTRAINT uq_leave_requests_number
        UNIQUE (
            tenant_id,
            request_number
        )

);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX idx_leave_requests_employee
    ON leave_requests(employee_id);

CREATE INDEX idx_leave_requests_assignment
    ON leave_requests(employee_leave_assignment_id);

CREATE INDEX idx_leave_requests_balance
    ON leave_requests(employee_leave_balance_id);

CREATE INDEX idx_leave_requests_status
    ON leave_requests(status);

CREATE INDEX idx_leave_requests_dates
    ON leave_requests(
        employee_id,
        leave_start_date,
        leave_end_date
    );

CREATE INDEX idx_leave_requests_pending
    ON leave_requests(
        tenant_id,
        status
    );

COMMIT;